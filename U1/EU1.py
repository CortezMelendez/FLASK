#veryficar version de python 
##python3 --version
#python3 -m venv venv 
##Buscamos la carpeta scripts en windows o bin en mac 
#. venv/bin/activate
##Debe aparecer al inicio del path entre parentesis venv

from flask import Flask, jsomifly

app= Flask(__name__)

#Endpoint HTML
@app.route('/')
def inicio():
    return """
<html>
<body>
<h1>Hola Mundo</>
<a href="http://127.0.0.1:500/api/saludo"> Buscar datos</>
</body>
</html>
"""

#pip install para hacer la instalacion de FLASK
#pip list vemos librerias en el proyecto
#pip install dotenv
#pip freeze agrega las librerias asociadas del proyeto a un archivo de requirements.txt
#la forma de instalacion de python es python3 app.py