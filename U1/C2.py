# Lista que contiene los días de la semana ordenados de Lunes a Domingo
week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Lista vacía para almacenar los índices correspondientes al fin de semana
out = []

# Bucle for que recorre la lista 'week' obteniendo el índice (i) y el valor (day)
for i, day in enumerate(week):
    # print(i, day)  

    # Evalúa si el día actual es "Sábado" o "Domingo"
    if day == "Sábado" or day == "Domingo":
        out.append(i)  # Guarda el número del índice en la lista 'out'

# Muestra en consola la lista resultante con los índices guardados: [5, 6]
print(out)