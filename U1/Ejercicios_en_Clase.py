
#Función que permita ingresar elementos a una lista dentro de un ciclo FOR.
listA=[]
def funcion1():
    for i  in range(1,20,3):
        listA.append(i)
    return(listA)
print (funcion1())


#Función que permita ingresar elementos a un diccionario dentro de un ciclo FOR.
diccA = {
}
def funcion2(diccA):
    """
        funcion2 | Carlos Cortez | 11/09/2026 
    
        Modified: 
        11/09/2026 - Carlos Cortez - Second function
    
        Parameters
        diccA = diccionario de datos
    
        Return: 
        Diccionario
        """
    for i in range (1,10):
        if i==2:
            diccA["Nombre"]={"Primer Nombre":"Carlos"}
        if i==7:
            diccA["Apellido"]={"Primer Apellido": "Cortez"}
        if i==9:
            diccA["Edad"]={"Numero":23}
    return(diccA)
print(funcion2(diccA))


#Función que permita imprimir todos los elementos de una lista y un diccionario dentro de un ciclo FOR.
def funcion3(lista, diccionario):
    print("Elementos de la lista:")
    for elemento in lista:
        print(elemento)
    print("\nElementos del diccionario:")
    for llave, valor in diccionario.items():
        print(llave)
        for llave2, valor2 in valor.items():
            print(llave2, ":", valor2)
    return
print(funcion3(listA, diccA))