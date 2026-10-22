#Diccionarios
#Relacion entrea llaves y valores

#.get 
#.values
#.items
#.update

#Ejemplo de diccionario

#network_config={
#    "IP": "172.0.0.1",
#    "Device": "Router",
#    "Policy": "Allow All",
#    "Status": True
#}

#Los diccionarios permiten que cualquier tipo de valor sean utiliizables, string, enteros, flotantes


#Actividad hacer al menos 5 diccionarios de dispositivos 

network_config_2={
    "0001": {
        "ip":"192.168.0.2",
        "device":"Switch",
        "policy":"Deny All",
        "status":False
    },
    "0002": {
        "ip":"192.168.0.1",
        "device":"Firewall",
        "policy":"Avoid .2.3.4",
        "status":True
    },
    "0003": {
        #Allow all es permitir todo
        "ip":"192.168.0.3",
        "device":"Router",
        "policy":"Allow All",
        "status":True
    },
    "0004": {
        "ip":"192.168.0.4",
        "device":"Access Point",
        "policy":"Allow All",
        "status":True
    },
    "0005": {
        #Deny All es denegar todo
        "ip":"192.168.0.5",
        "device":"Server",
        "policy":"Deny All",
        "status":False,
        "lista": [1,4,6,0,8]
    }
}

#Imprimir la posición 3 de la lista a que contiene un diccionario
a=[1,2,3,[7.8,1]]
#print(a[3])
#para imprimir la siguiente posicion dentro de la lista es 
#print(a[3][1])

#imprimir el valor de la llave ip del diccionario 0001
#print(network_config_2.get("0001"))

#Imprimimos de la clave 0005 el valor de la llave lista y de esa lista imprimimos la posición 2
#mandando a llamar el indice de la lista que es 2 y el valor que contiene es 6
#print (network_config_2.get("0005").get("lista")[2])

#Primero se extrae el diccionario o valor del 0005
contenido=network_config_2.get("0005")
#Byusca la clave lista y regresa el valor de esta
listaA=contenido.get("lista")
#busca un elemento de la lista con el indice 
num= listaA[2]
print(num)

network_config_2["0008"]={"ip":1}
print(network_config_2)
    