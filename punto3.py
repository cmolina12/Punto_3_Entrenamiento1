
import pulp as pl
import matplotlib.pyplot as plt

import pulp as pl

# Conjuntos
cultivos = ["LB", "TSA", "MRS", "SDA"]  
nutrientes = ["Agar", "Levadura", "Peptona", "NaCl", "Fosfato"] 
recursos = ["Fosfato", "Péptidos", "Aminoácidos", "Extracto de Levadura", "Agar"] #

# Parámetros
minimo = {"LB": {"Agar": 8.4, "Levadura": 1.26, "Peptona": 10.22, "NaCl": 3, "Fosfato": 0},
          "TSA": {"Agar": 4.33, "Levadura": 1.42, "Peptona": 5.3, "NaCl": 1.26, "Fosfato": 0},
          "MRS": {"Agar": 1.2, "Levadura": 0, "Peptona": 0.8, "NaCl": 0.025, "Fosfato": 0.8},
          "SDA": {"Agar": 0, "Levadura": 0, "Peptona": 0.5, "NaCl": 0, "Fosfato": 0}} #Porcentaje minimo de cada nutriente en cada cultivo

maximo = {"LB": {"Agar": 19, "Levadura": 22.8, "Peptona": 36, "NaCl": 10, "Fosfato": 0},
          "TSA": {"Agar": 26.1, "Levadura": 15.4, "Peptona": 46, "NaCl": 10, "Fosfato": 0},
          "MRS": {"Agar": 11, "Levadura": 0, "Peptona": 11.4, "NaCl": 1, "Fosfato": 72},
          "SDA": {"Agar": 25, "Levadura": 0, "Peptona": 74, "NaCl": 0, "Fosfato": 0}} #Porcentaje maximo de cada nutriente en cada cultivo

disponibilidad = {"Fosfato": 206, "Péptidos": 641, "Aminoácidos": 120, 
                 "Extracto de Levadura": 145, "Agar": 189} #Cantidad disponible de cada recurso

costo = {"Fosfato": 323, "Péptidos": 510, "Aminoácidos": 119, 
         "Extracto de Levadura": 340, "Agar": 826} #Costo de cada recurso

composicion = {"Fosfato": {"Agar": 0, "Levadura": 0, "Peptona": 0, "NaCl": 0, "Fosfato": 100},
               "Péptidos": {"Agar": 0, "Levadura": 0, "Peptona": 70, "NaCl": 0, "Fosfato": 0},
               "Aminoácidos": {"Agar": 0, "Levadura": 0, "Peptona": 48, "NaCl": 0, "Fosfato": 52},
               "Extracto de Levadura": {"Agar": 0, "Levadura": 76, "Peptona": 0, "NaCl": 13, "Fosfato": 0},
               "Agar": {"Agar": 84, "Levadura": 0, "Peptona": 0, "NaCl": 5, "Fosfato": 0}} #Composicion de cada recurso

modelo = pl.LpProblem("Minimizar", pl.LpMinimize)

# Variables
x = pl.LpVariable.dicts("x", (cultivos, recursos), lowBound=0, cat="Continuous") #Cantidad de recurso r utilizado para el cultivo c

# Función objetivo
modelo += pl.lpSum([x[c][r] * costo[r] for c in cultivos for r in recursos]) #Se busca minimizar el costo total que es la suma del costo de cada recurso utilizado

#Restricciones

#Disponibilidad de recursos
for r in recursos: #Para cada recurso
    modelo += pl.lpSum([x[c][r] for c in cultivos]) <= disponibilidad[r] #Restriccion de disponibilidad, la cantidad de recurso utilizado debe ser menor o igual a la cantidad disponible
    
#Produccion total de cada cultivo
for c in cultivos: #Para cada cultivo
    modelo += pl.lpSum([x[c][r] for r in recursos]) == 300 #Restriccion de produccion total, se deben producir 300 kg de cada cultivo

#Restricciones de nutrientes

for c in cultivos: #Para cada cultivo
    total_mix = pl.lpSum([x[c][r] for r in recursos]) #Cantidad total de mezcla
    for n in nutrientes: #Para cada nutriente
        total_nutrient = pl.lpSum([(x[c][r] * composicion[r][n]) for r in recursos]) #Cantidad total de nutriente en la mezcla
        modelo += total_nutrient >= minimo[c][n] * total_mix #Restriccion minima, el porcentaje de nutriente en la mezcla debe ser mayor o igual al minimo
        modelo += total_nutrient <= maximo[c][n] * total_mix #Restriccion maxima, el porcentaje de nutriente en la mezcla debe ser menor o igual al maximo
#Imprimir
modelo.solve()

#Imprimir resultados, indicar la cantidad de cada recurso que se debe utilizar para cada cultivo, ademas de los porcentajes de cada nutriente en la mezcla final

for c in cultivos:
    print(f"Para el cultivo {c} se deben utilizar:")
    for r in recursos:
        print(f"{round(x[c][r].varValue,2)} kg de {r}")
    total_mix = pl.lpSum([x[c][r].varValue for r in recursos])
    print("")
    for n in nutrientes:
        total_nutrient = pl.lpSum([(x[c][r].varValue * composicion[r][n]) for r in recursos])
        print(f"El porcentaje de {n} en la mezcla final es: {round(pl.value(total_nutrient / total_mix),2)}%")
    print("\n")

print(f"El costo total es: ${round(pl.value(modelo.objective),2)}")

#Grafica 

#Se grafica la cantidad de cada recurso que se debe utilizar para cada cultivo
for r in recursos:
    plt.bar(cultivos, [x[c][r].varValue for c in cultivos], label=r)
plt.title("Cantidad de cada recurso que se debe utilizar para cada cultivo")
plt.xlabel("Cultivo")
plt.ylabel("Cantidad (kg)")
plt.legend()
plt.show()

#Se grafica el porcentaje de cada nutriente en la mezcla final
for n in nutrientes:
    plt.bar(cultivos, [pl.value(pl.lpSum([(x[c][r].varValue * composicion[r][n])/100 for r in recursos]) / pl.value(pl.lpSum([x[c][r].varValue for r in recursos])) * 100) for c in cultivos], label=n)
plt.title("Porcentaje de cada nutriente en la mezcla final")
plt.xlabel("Cultivo")  
plt.ylabel("Porcentaje (%)")
plt.legend()
plt.show()


