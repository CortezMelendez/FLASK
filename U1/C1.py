# Asignación de la variable 'a'
a = 1

# Definición de la función find_n que recibe el argumento 'a'
def find_n(a):
    """
    find-n | Carlos Cortez | 03/09/2026 

    Modified: 
    03/09/2026 - Carlos Cortez - Initial implementation

    Parameters
    a int

    Return: 
    string
    """

    # if(a):               # Estructura condicional (desactivada/comentada)
    print(type(a))        # Muestra el tipo de dato que recibe la función (<class 'int'>)
    # return str(a)        # Retorno de valor (desactivado; la función regresa None por defecto)

# Llamada a la función pasando 'a' (1) e imprimiendo su resultado ('None')
print(find_n(a))


# Definición de una lista con 5 elementos de tipo string
Lista_a = ["A", "B", "C", "D", "E"]

# Definición de una variable de tipo cadena de texto (string)
abc = "ABCDE"

# Imprime el primer elemento de la lista usando el índice 0 ('A')
print(Lista_a[0])

# Imprime una subcadena desde el índice 2 ('C') hasta el penúltimo carácter sin incluir el último ('CD')
print(abc[2:-1])

