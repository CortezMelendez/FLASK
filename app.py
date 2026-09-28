#veryficar version de python 
##python3 --version
#python3 -m venv venv 
##Buscamos la carpeta scripts en windows o bin en mac 
#. venv/bin/activate
##Debe aparecer al inicio del path entre parentesis venv
from flask import Flask, jsonify
import json

with open("API.json", "r") as json_api:
    datos_json = json.load(json_api)

app = Flask(__name__)

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

# Endpoint JSON
@app.route('/servidor_1')
def servidor_1():
    return jsonify({
    "0001": {
        "ip": "192.168.0.1",
        "divice": "Router",
        "policy": ["Ro", "Not Allowed", [0.2, 0.3, 0.5] ],
        "status": True,
    }
})

if __name__ == '__main__':
    app.run(debug=True)


#Hacer 10 funciones de tipo get 1 por cada funcion # Ir cambiando datos 
#Hacer ciclos con datos de funciones quien la hace cuando la modifica 
#5 para mostrar elementos del diccionario
#5 para inventar datos
