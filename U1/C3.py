nums=["uno", "dos", "tres", "cuatro","cinco","seis","siete","ocho","nueve","diez"]
colors=["rojo", "azul","verde","amarillo","naranja","morado","rosa","negro","blanco","gris"]

#print(nums)
#colors.append("celeste")
#colors.extend(["celeste", "gris"])
#print(colors.pop(0))
#colors.sort(reverse=False)
#colors_1=colors.copy()
#print(colors_1)

#.append envia a la parte final de la lista
#.extend Permite agregar mas datos a la lista
#.insert (posicion, elemento) se coloca la posicion donde quieras que se agregue el elemento
#y se agrega en esa posicion##
#.clear elimina toda la lista y la deja vacia sin eliminar la variable
#.pop Extrae el elemento de la lista 
#.sort Ordena la lista por orden alfabetico con valor false empieza con la letra a y 
#y true inicia con la ultima letra del alfabeto de la lista 
#.copy realiza una copia de la variable

#Iterar entre colores y numeros es decir numero color numero color

#for num in nums:
#insercion variables de datos, dentro de las llaves se asigna valor de variable
#out = f"Number: {num}"


#out= f"[{num}, {colors[nums.index(num)]}]" 
#print (out)
    

#Imprimir la iteracion de la lista de numeros y colores en una sola linea
#print ([nums[0], colors[0]])


#Actividad
#invierte la lista de nums para poder ver los elementod de la lizta ['diez','rojo']
#Al final crea una nueva lista de ambos elementos e imprime la nueva lista

list_new = []
nums.reverse()
for num in nums:

    salida = f"[{num}, {colors[nums.index(num)]}]" 
    #print (salida)
    list_new.append(salida)

print(list_new)
