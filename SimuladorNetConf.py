from flask import Flask, request, Response
import json

app = Flask(__name__)

# Base de datos simulada (Configuración de la interfaz)
network_config = {
    "ietf-interfaces:interfaces": {
        "interface": [
            {
                "name": "GigabitEthernet1",
                "description": "Enlace Principal",
                "type": "iana-if-type:ethernetCsmacd",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {
                            "ip": "192.168.1.1",
                            "netmask": "255.255.255.0"
                        }
                    ]
                }
            }
        ]
    }
}

# =====================================================================
# SIMULACIÓN RESTCONF (Usa HTTP estándar + JSON/YANG)
# =====================================================================
@app.route('/restconf/data/ietf-interfaces:interfaces', methods=['GET'])
def get_restconf():
    # Devuelve la configuración en formato JSON (Media Type de RESTCONF)
    return Response(
        json.dumps(network_config), 
        status=200, 
        mimetype='application/yang-data+json'
    )

@app.route('/restconf/data/ietf-interfaces:interfaces', methods=['PUT'])
def put_restconf():
    global network_config
    if not request.is_json:
        return Response('{"error": "Debe ser JSON"}', status=400, mimetype='application/yang-data+json')
    
    # Actualiza la configuración
    network_config = request.get_json()
    return Response(status=204)


# =====================================================================
# SIMULACIÓN NETCONF (Expuesta vía HTTP para pruebas en Postman)
# =====================================================================
@app.route('/netconf/rpc', methods=['POST'])
def netconf_rpc():
    xml_data = request.data.decode('utf-8')
    
    # Validar si es una solicitud <get-config>
    if "<get-config>" in xml_data:
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>GigabitEthernet1</name>
        <enabled>true</enabled>
      </interface>
    </interfaces>
  </data>
</rpc-reply>"""
        return Response(xml_response, status=200, mimetype='application/xml')
    
    # Validar si es una solicitud <edit-config>
    elif "<edit-config>" in xml_data:
        xml_response = """<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply message-id="102" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ok/>
</rpc-reply>"""
        return Response(xml_response, status=200, mimetype='application/xml')
    
    # Respuesta por defecto si no se reconoce el RPC
    error_response = """<?xml version="1.0" encoding="UTF-8"?>
<rpc-reply message-id="100" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <rpc-error>
    <error-type>application</error-type>
    <error-tag>operation-not-supported</error-tag>
    <error-severity>error</error-severity>
  </rpc-error>
</rpc-reply>"""
    return Response(error_response, status=400, mimetype='application/xml')

if __name__ == '__main__':
    # Corre el servidor en el puerto 5000
    app.run(debug=True, port=5000)
