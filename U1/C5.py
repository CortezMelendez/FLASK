#Para hacer un for tipico utilizamos un for i in range (numero hasta donde itera#)
#EJ. for i in range (5,15)


#En el range tambien se pueden hacer saltos , range (1,10,2)
#El primero es donde empieza, el segundo es hasta donde llega y el tercero de cuanto en cuanto


from flask import Flask, jsonify

app = Flask(__name__)

# Diccionario global con los 5 elementos base
dispositivos = {
    101: {
        "ip": "192.168.1.10",
        "device_name": "Router Principal",
        "policy": {"type": "ALLOW_ALL"},
        "status": "Activo"
    },
    102: {
        "ip": "192.168.1.20",
        "device_name": "Switch Piso 1",
        "policy": {"type": "BLOCK_IP", "blocked_ip": "192.168.1.20"},
        "status": "Activo"
    },
    103: {
        "ip": "192.168.1.30",
        "device_name": "Firewall",
        "policy": {"type": "REQUIRED_IP", "required_ip": "192.168.1.30"},
        "status": "Activo"
    },
    104: {
        "ip": "192.168.1.40",
        "device_name": "Servidor Web",
        "policy": {"type": "REQUIRED_IP", "required_ip": "192.168.1.50"},
        "status": "Inactivo"
    },
    105: {
        "ip": "192.168.1.50",
        "device_name": "Access Point",
        "policy": {"type": "ALLOW_ALL"},
        "status": "Activo"
    }
}

# Endpoint HTML de inicio
@app.route('/')
def inicio():
    return """
<html>
<body>
<h1>Hola Mundo</h1>
<a href="http://127.0.0.1:5000/api/saludo">Buscar datos</a>
</body>
</html>
"""

# Endpoint principal
@app.route('/api/saludo')
def saludo():
    return jsonify(dispositivos)


# ==============================================================================
# SECCIÓN 1: 5 FUNCIONES GET PARA MOSTRAR UN ELEMENTO EXISTENTE
# ==============================================================================

@app.route('/api/mostrar/router', methods=['GET'])
def mostrar_router():
    """
    mostrar_router | Carlos Cortez | 03/09/2026 

    Modified: 
    03/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    return jsonify({101: dispositivos[101]})


@app.route('/api/mostrar/switch', methods=['GET'])
def mostrar_switch():
    """
    mostrar_switch | Carlos Cortez | 04/09/2026 

    Modified: 
    04/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    return jsonify({102: dispositivos[102]})


@app.route('/api/mostrar/firewall', methods=['GET'])
def mostrar_firewall():
    """
    mostrar_firewall | Carlos Cortez | 05/09/2026 

    Modified: 
    05/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    return jsonify({103: dispositivos[103]})


@app.route('/api/mostrar/servidor', methods=['GET'])
def mostrar_servidor():
    """
    mostrar_servidor | Carlos Cortez | 06/09/2026 

    Modified: 
    06/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    return jsonify({104: dispositivos[104]})


@app.route('/api/mostrar/accesspoint', methods=['GET'])
def mostrar_access_point():
    """
    mostrar_access_point | Carlos Cortez | 07/09/2026 

    Modified: 
    07/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    return jsonify({105: dispositivos[105]})


# ==============================================================================
# SECCIÓN 2: 5 FUNCIONES GET PARA INVENTAR Y AGREGAR UN ELEMENTO AL DICCIONARIO
# ==============================================================================

@app.route('/api/agregar/impresora', methods=['GET'])
def agregar_impresora():
    """
    agregar_impresora | Carlos Cortez | 08/09/2026 

    Modified: 
    08/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    nuevo_id = 106
    dispositivos[nuevo_id] = {
        "ip": "192.168.1.60",
        "device_name": "Impresora de Red",
        "policy": {"type": "ALLOW_ALL"},
        "status": "Activo"
    }
    return jsonify({nuevo_id: dispositivos[nuevo_id]})


@app.route('/api/agregar/nas', methods=['GET'])
def agregar_nas():
    """
    agregar_nas | Carlos Cortez | 09/09/2026 

    Modified: 
    09/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    nuevo_id = 107
    dispositivos[nuevo_id] = {
        "ip": "192.168.1.70",
        "device_name": "Servidor NAS Almacenamiento",
        "policy": {"type": "RESTRICTED", "allowed_users": ["admin"]},
        "status": "Activo"
    }
    return jsonify({nuevo_id: dispositivos[nuevo_id]})


@app.route('/api/agregar/camara', methods=['GET'])
def agregar_camara():
    """
    agregar_camara | Carlos Cortez | 10/09/2026 

    Modified: 
    10/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    nuevo_id = 108
    dispositivos[nuevo_id] = {
        "ip": "192.168.1.80",
        "device_name": "Cámara de Seguridad IP",
        "policy": {"type": "STREAM_ONLY"},
        "status": "Activo"
    }
    return jsonify({nuevo_id: dispositivos[nuevo_id]})


@app.route('/api/agregar/ups', methods=['GET'])
def agregar_ups():
    """
    agregar_ups | Carlos Cortez | 11/09/2026 

    Modified: 
    11/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    nuevo_id = 109
    dispositivos[nuevo_id] = {
        "ip": "192.168.1.90",
        "device_name": "UPS Respaldos de Energía",
        "policy": {"type": "MONITOR_ONLY"},
        "status": "Inactivo"
    }
    return jsonify({nuevo_id: dispositivos[nuevo_id]})


@app.route('/api/agregar/sensor', methods=['GET'])
def agregar_sensor():
    """
    agregar_sensor | Carlos Cortez | 12/09/2026 

    Modified: 
    12/09/2026 - Carlos Cortez - Initial implementation

    Parameters:
    Ninguno

    Return: 
    json
    """
    nuevo_id = 110
    dispositivos[nuevo_id] = {
        "ip": "192.168.1.100",
        "device_name": "Sensor de Temperatura DataCenter",
        "policy": {"type": "IOT_DEVICE"},
        "status": "Activo"
    }
    return jsonify({nuevo_id: dispositivos[nuevo_id]})


if __name__ == '__main__':
    app.run(debug=True)