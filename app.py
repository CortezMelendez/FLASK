import ipaddress
import json
import os
import re
import tempfile
from pathlib import Path

from filelock import FileLock
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFError, CSRFProtect

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "API.json"
DATA_LOCK = FileLock(str(JSON_FILE) + ".lock")
MAX_ELEMENTS = 1000

PROTOCOL_OPTIONS = ["STP", "OSPF", "BGP", "EIGRP", "RIP"]
ALLOWED_STATES = {"online", "offline", "maintenance", "warning"}
ALLOWED_POLICIES = {"SSH", "ACL", "VLAN", "STP", "TELNET", "ROUTING", "MONITORING", "POLICY"}
SQL_KEYWORDS = ("SELECT", "DROP", "UNION", "INSERT", "UPDATE", "DELETE", "ALTER", "--", ";", "/*", "*/")

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 -]{0,49}$")
VLAN_NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,20}$")
PORT_RE = re.compile(r"^(Gi|Fa|Se|Te|Eth|Lo|Po)\d+(\/\d+){1,3}$", re.IGNORECASE)
POLICY_VALUE_RE = re.compile(r"^POL_\d{1,5}$")


def sanitize_for_log(value):
    if value is None:
        return ""
    return str(value).replace("\r", "").replace("\n", "")


def contains_sql_keyword(value):
    text = (value or "").upper()
    return any(keyword in text for keyword in SQL_KEYWORDS)


def normalize_mac(value):
    value = (value or "").strip().upper().replace("::", ":")
    while "::" in value:
        value = value.replace("::", ":")
    return value


def valid_mac(value):
    cleaned = normalize_mac(value)
    if not cleaned:
        return False
    if not re.fullmatch(r"(?:[A-F0-9]{2}:){4,5}[A-F0-9]{2}", cleaned):
        return False
    if len(cleaned) > 17:
        return False
    return True


def valid_name(value):
    text = (value or "").strip()
    if not text or not NAME_RE.fullmatch(text):
        return False
    if not re.match(r"^[A-Za-z]", text):
        return False
    if contains_sql_keyword(text):
        return False
    return True


def valid_vlan_name(value):
    text = (value or "").strip()
    if not text or not VLAN_NAME_RE.fullmatch(text):
        return False
    if contains_sql_keyword(text):
        return False
    return True


def valid_ip(value):
    text = (value or "").strip()
    if not text or len(text) > 15 or not re.fullmatch(r"\d+(?:\.\d+){3}", text):
        return False
    parts = text.split('.')
    if len(parts) != 4:
        return False
    try:
        octets = [int(part) for part in parts]
    except ValueError:
        return False
    for part in octets:
        if not 0 <= part <= 255:
            return False
    if text in {"0.0.0.0", "0.0.0.1", "255.255.255.255"}:
        return False
    if octets[0] == 0 or octets[0] == 127 or (octets[0] == 169 and octets[1] == 254):
        return False
    if octets[0] >= 224:
        return False
    return True


def valid_state(value):
    return (value or "").strip() in ALLOWED_STATES


def valid_protocols(values):
    norms = []
    for item in values or []:
        val = (item or "").strip().upper()
        if val in PROTOCOL_OPTIONS:
            norms.append(val)
        else:
            return False, []
    return True, norms


def split_csv(value):
    if value is None:
        return []
    return [part.strip() for part in str(value).split(",") if part and part.strip()]


def valid_ports(raw_value):
    items = split_csv(raw_value)
    if not items:
        return True, []
    normalized = []
    for item in items:
        value = item.strip().upper()
        if len(value) > 20 or not PORT_RE.fullmatch(value):
            return False, []
        normalized.append(value)
    return True, normalized


def valid_policies(raw_value):
    items = split_csv(raw_value)
    if not items:
        return True, []
    normalized = []
    for item in items:
        value = item.strip().upper()
        if len(value) > 20 or (value not in ALLOWED_POLICIES and not POLICY_VALUE_RE.fullmatch(value)):
            return False, []
        normalized.append(value)
    return True, normalized


def sanitize_search_text(value):
    if value is None:
        return ""
    cleaned = re.sub(r"[^A-Za-z0-9\s:._/-]", "", str(value)).strip()
    return cleaned[:80]


def add_error(errors, field, message):
    errors.append({"field": field, "message": message})


def validate_element_form(form):
    errors = []

    mac_raw = (form.get("mac") or "").strip()
    normalized_mac = normalize_mac(mac_raw)
    if not valid_mac(mac_raw):
        add_error(errors, "mac", "Invalid MAC format. Use XX:XX:XX:XX:XX:XX or AA::10C::7D::01.")
    else:
        mac_raw = normalized_mac

    name_raw = (form.get("name") or "").strip()
    if not valid_name(name_raw):
        add_error(errors, "name", "Name must start with a letter and contain only letters, numbers, spaces, or hyphens.")

    ip_raw = (form.get("ip") or "").strip()
    if not valid_ip(ip_raw):
        add_error(errors, "ip", "The IP address is not valid.")

    state_raw = (form.get("status") or "").strip()
    if not valid_state(state_raw):
        add_error(errors, "status", "Unrecognized state.")

    selected_protocols = form.getlist("protocols")
    ok_protocols, protocols = valid_protocols(selected_protocols)
    if not ok_protocols or not protocols:
        add_error(errors, "protocols", "One or more protocols are not valid.")

    vlan_names = form.getlist("vlan_name[]")
    vlan_ips = form.getlist("vlan_ip[]")
    vlan_ports = form.getlist("vlan_ports[]")
    vlan_policies = form.getlist("vlan_policies[]")
    max_len = max(len(vlan_names), len(vlan_ips), len(vlan_ports), len(vlan_policies), 0)

    if max_len > 10:
        add_error(errors, "vlans", "A maximum of 10 VLAN blocks is allowed.")
        max_len = 10

    vlans = []
    for index in range(max_len):
        name_value = vlan_names[index].strip() if index < len(vlan_names) else ""
        ip_value = vlan_ips[index].strip() if index < len(vlan_ips) else ""
        ports_value = vlan_ports[index] if index < len(vlan_ports) else ""
        policies_value = vlan_policies[index] if index < len(vlan_policies) else ""

        block_has_data = bool(name_value or ip_value or ports_value or policies_value)
        if not block_has_data:
            continue

        if not valid_vlan_name(name_value):
            add_error(errors, "vlan_name", "Invalid VLAN name (max. 20 characters, no spaces).")

        if not valid_ip(ip_value):
            add_error(errors, "vlan_ip", "The VLAN IP is not valid.")

        ok_ports, port_list = valid_ports(ports_value)
        if not ok_ports:
            add_error(errors, "ports", "One or more ports have an invalid format (e.g. Gi0/0).")

        ok_policies, policy_list = valid_policies(policies_value)
        if not ok_policies:
            add_error(errors, "policies", "One or more policies are not valid.")

        vlans.append({
            "vlan_name": name_value,
            "ipv4_address": ip_value,
            "ports": port_list,
            "policies": policy_list,
        })

    if not errors:
        return {
            "mac": mac_raw,
            "name": name_raw,
            "ip": ip_raw,
            "status": state_raw,
            "protocols": protocols,
            "vlans": vlans,
        }, []

    return None, errors


def read_json_data():
    if not JSON_FILE.exists():
        return {}
    with DATA_LOCK:
        with JSON_FILE.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    if not isinstance(data, dict):
        return {}
    return data


def write_json_data(data):
    with DATA_LOCK:
        temp_fd, temp_path = tempfile.mkstemp(dir=str(BASE_DIR), prefix="api_", suffix=".tmp")
        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=4, ensure_ascii=False)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temp_path, 0o600)
            os.replace(temp_path, JSON_FILE)
            os.chmod(JSON_FILE, 0o600)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


def load_or_create_data():
    data = read_json_data()
    if not isinstance(data, dict):
        return {}
    return data


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["DEBUG"] = False
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["WTF_CSRF_TIME_LIMIT"] = 3600
csrf = CSRFProtect(app)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@app.after_request
def apply_security_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store, no-cache"
    return response


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(_):
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(CSRFError)
def handle_csrf(_):
    return jsonify({"field": "csrf", "message": "Invalid CSRF token."}), 400


@app.errorhandler(TypeError)
@app.errorhandler(ValueError)
@app.errorhandler(KeyError)
def handle_validation_errors(_):
    return jsonify({"field": "general", "message": "Bad request."}), 400


@app.route("/", methods=["GET"])
def inicio():
    return redirect(url_for("tabla_elementos"))


@app.route("/tabla_elementos", methods=["GET"])
@limiter.limit("30/minute")
def tabla_elementos():
    datos = load_or_create_data()
    search_value = sanitize_search_text(request.args.get("q", ""))
    rows = []

    for mac, item in datos.items():
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip() or "N/A"
        ip_value = str(item.get("ip", "")).strip() or "N/A"
        vlans = item.get("vlans") if isinstance(item.get("vlans"), list) else []
        vlan_names = ", ".join(v.get("vlan_name", "") for v in vlans if isinstance(v, dict) and v.get("vlan_name"))
        vlan_ips = ", ".join(v.get("ipv4_address", "") for v in vlans if isinstance(v, dict) and v.get("ipv4_address"))
        search_text = " ".join([mac, name, ip_value, vlan_names, vlan_ips]).lower()
        if search_value and search_value.lower() not in search_text:
            continue

        first_vlan = vlans[0] if vlans and isinstance(vlans[0], dict) else {}
        rows.append({
            "mac": mac,
            "name": name,
            "status": item.get("status", "online"),
            "protocolos": ", ".join(item.get("protocols", [])) or "N/A",
            "vlan": vlan_names or "N/A",
            "ip": first_vlan.get("ipv4_address", ip_value),
            "ports": ", ".join(first_vlan.get("ports", [])) or "N/A",
            "policies": ", ".join(first_vlan.get("policies", [])) or "N/A",
        })

    return render_template("tabla_elementos.html", rows=rows, filtro=search_value)


@app.route("/formulario_elemento", methods=["GET"])
def formulario_elemento():
    return render_template(
        "formulario_elemento.html",
        item=None,
        action=url_for("guardar_elemento"),
        protocols=PROTOCOL_OPTIONS,
    )


@app.route("/formulario_elemento/<id>", methods=["GET"])
def formulario_elemento_editar(id):
    datos = load_or_create_data()
    item = datos.get(id)
    if not item:
        return redirect(url_for("tabla_elementos"))
    return render_template(
        "formulario_elemento.html",
        item=item,
        action=url_for("guardar_elemento"),
        protocols=PROTOCOL_OPTIONS,
    )


@app.route("/guardar_elemento", methods=["POST"])
@limiter.limit("10/minute")
def guardar_elemento():
    if request.mimetype not in {"application/x-www-form-urlencoded", "multipart/form-data"}:
        return jsonify({"field": "content-type", "message": "Unsupported content type."}), 400

    registro, errors = validate_element_form(request.form)
    if errors:
        return jsonify(errors), 400

    datos = load_or_create_data()
    normalized_mac = normalize_mac(request.form.get("mac", ""))
    if len(datos) >= MAX_ELEMENTS and normalized_mac not in datos:
        return jsonify({"field": "general", "message": "Maximum number of elements reached."}), 400

    datos[normalized_mac] = registro
    write_json_data(datos)
    return redirect(url_for("tabla_elementos"))


@app.route("/eliminar_elemento/<id>", methods=["POST"])
@limiter.limit("10/minute")
def eliminar_elemento(id):
    if request.mimetype not in {"application/x-www-form-urlencoded", "multipart/form-data"}:
        return jsonify({"field": "content-type", "message": "Unsupported content type."}), 400

    data = load_or_create_data()
    if id in data:
        del data[id]
        write_json_data(data)
    return redirect(url_for("tabla_elementos"))


@app.route("/ver_elemento/<id>", methods=["GET"])
def ver_elemento(id):
    datos = load_or_create_data()
    item = datos.get(id)
    if not item:
        return redirect(url_for("tabla_elementos"))
    return render_template("ver_elemento.html", item=item, id=id)


@app.route("/json/<mac>", methods=["GET"])
def json_data(mac):
    datos = load_or_create_data()
    item = datos.get(mac)
    if item is None:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(item)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
