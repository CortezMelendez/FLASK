# verificar version de python 
## python3 --version
# python3 -m venv venv 
## Buscamos la carpeta scripts en windows o bin en mac 
#. venv/bin/activate
## Debe aparecer al inicio del path entre parentesis venv

from flask import Flask, jsonify
import json

# Cargar archivo JSON base
with open("API.json", "r") as json_api:
    datos_json = json.load(json_api)

app = Flask(__name__)

# Diccionario base de servidores / dispositivos
servidores = {
    "0001": {
        "ip": "192.168.0.1",
        "device": "Router Principal",
        "policy": ["Ro", "Not Allowed", [0.2, 0.3, 0.5]],
        "status": True
    },
    "0002": {
        "ip": "192.168.0.2",
        "device": "Switch Piso 1",
        "policy": ["Rw", "Allowed"],
        "status": True
    },
    "0003": {
        "ip": "192.168.0.3",
        "device": "Firewall Core",
        "policy": ["Block All"],
        "status": True
    },
    "0004": {
        "ip": "192.168.0.4",
        "device": "Servidor Web",
        "policy": ["HTTP", "HTTPS"],
        "status": False
    },
    "0005": {
        "ip": "192.168.0.5",
        "device": "Access Point",
        "policy": ["WPA3"],
        "status": True
    }
}

# ==============================================================================
# ENDPOINTS INICIALES
# ==============================================================================

# Endpoint HTML
@app.route('/')
def inicio():
    print("Cambio")
    return datos_json["AB::10C::7D::"]

@app.route('/json/<mac>')
def json_data(mac):
    print(datos_json[mac]["name"])
    print(datos_json[mac]["protocolos"])
    print(datos_json[mac]["vlans"])
    print(datos_json[mac]["status"])
    return datos_json[mac]["name"]


# ==============================================================================
# SECCIÓN 1: 5 FUNCIONES GET PARA MOSTRAR ELEMENTOS DEL DICCIONARIO
# ==============================================================================

@app.route('/servidor_1', methods=['GET'])
def servidor_1():
    """
    servidor_1 | Carlos Cortez | 03/09/2026 
    Modified: 03/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    return jsonify({"0001": servidores["0001"]})


@app.route('/servidor_2', methods=['GET'])
def servidor_2():
    """
    servidor_2 | Carlos Cortez | 04/09/2026 
    Modified: 04/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    return jsonify({"0002": servidores["0002"]})


@app.route('/servidor_3', methods=['GET'])
def servidor_3():
    """
    servidor_3 | Carlos Cortez | 05/09/2026 
    Modified: 05/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    return jsonify({"0003": servidores["0003"]})


@app.route('/servidor_4', methods=['GET'])
def servidor_4():
    """
    servidor_4 | Carlos Cortez | 06/09/2026 
    Modified: 06/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    return jsonify({"0004": servidores["0004"]})


@app.route('/servidor_5', methods=['GET'])
def servidor_5():
    """
    servidor_5 | Carlos Cortez | 07/09/2026 
    Modified: 07/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    return jsonify({"0005": servidores["0005"]})


# ==============================================================================
# SECCIÓN 2: 5 FUNCIONES GET PARA INVENTAR Y AGREGAR DATOS AL DICCIONARIO
# ==============================================================================

@app.route('/servidor_6', methods=['GET'])
def servidor_6():
    """
    servidor_6 | Carlos Cortez | 08/09/2026 
    Modified: 08/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    servidores["0006"] = {
        "ip": "192.168.0.6",
        "device": "Impresora de Red",
        "policy": ["Print Only"],
        "status": True
    }
    return jsonify({"0006": servidores["0006"]})


@app.route('/servidor_7', methods=['GET'])
def servidor_7():
    """
    servidor_7 | Carlos Cortez | 09/09/2026 
    Modified: 09/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    servidores["0007"] = {
        "ip": "192.168.0.7",
        "device": "Servidor NAS Almacenamiento",
        "policy": ["Backup", "Restricted"],
        "status": True
    }
    return jsonify({"0007": servidores["0007"]})


@app.route('/servidor_8', methods=['GET'])
def servidor_8():
    """
    servidor_8 | Carlos Cortez | 10/09/2026 
    Modified: 10/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    servidores["0008"] = {
        "ip": "192.168.0.8",
        "device": "Cámara IP Seguridad",
        "policy": ["Stream Only"],
        "status": True
    }
    return jsonify({"0008": servidores["0008"]})


@app.route('/servidor_9', methods=['GET'])
def servidor_9():
    """
    servidor_9 | Carlos Cortez | 11/09/2026 
    Modified: 11/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    servidores["0009"] = {
        "ip": "192.168.0.9",
        "device": "UPS Smart Respaldos",
        "policy": ["Monitor Only"],
        "status": False
    }
    return jsonify({"0009": servidores["0009"]})


@app.route('/servidor_10', methods=['GET'])
def servidor_10():
    """
    servidor_10 | Carlos Cortez | 12/09/2026 
    Modified: 12/09/2026 - Carlos Cortez - Initial implementation
    Parameters: Ninguno
    Return: json
    """
    servidores["0010"] = {
        "ip": "192.168.0.10",
        "device": "Sensor Telemetría DataCenter",
        "policy": ["IoT Device"],
        "status": True
    }
    return jsonify({"0010": servidores["0010"]})


if __name__ == '__main__':
    app.run(debug=True)