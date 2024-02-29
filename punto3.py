
import pulp as pl
import matplotlib.pyplot as plt

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

total_mezcla = 300 #Cantidad total de mezcla

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
    for n in nutrientes: #Para cada nutriente
        total_nutrient = pl.lpSum([(x[c][r] * (composicion[r][n]*0.01)) for r in recursos]) #Cantidad total de nutriente en la mezcla, se multiplica por 0.01 para convertir el entero a porcentaje
        modelo += total_nutrient >= (minimo[c][n]*0.01) * total_mezcla #Restriccion minima, el porcentaje de nutriente en la mezcla debe ser mayor o igual al minimo, se multiplica por 0.01 para convertir el entero a porcentaje
        modelo += total_nutrient <= (maximo[c][n]*0.01) * total_mezcla #Restriccion maxima, el porcentaje de nutriente en la mezcla debe ser menor o igual al maximo, se multiplica por 0.01 para convertir el entero a porcentaje
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

#Grafica de el cultivo LB
heights = [x["LB"][r].varValue for r in recursos] #Se obtiene la cantidad de cada recurso que se debe utilizar para el cultivo LB
bars = plt.bar(recursos, heights, color="blue", label="LB", alpha=0.5) #Se grafica la cantidad de cada recurso que se debe utilizar para el cultivo LB
for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor de la cantidad de cada recurso que se debe utilizar para el cultivo LB
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Cantidad de cada recurso que se debe utilizar para el cultivo LB") #Se coloca el titulo  
plt.xlabel("Recurso") #Se coloca el nombre del eje x
plt.ylabel("Cantidad (kg)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los recursos para que no se superpongan 
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica

#Grafica de el cultivo TSA
heights = [x["TSA"][r].varValue for r in recursos] #Se obtiene la cantidad de cada recurso que se debe utilizar para el cultivo TSA
bars = plt.bar(recursos, heights, color="red", label="TSA", alpha=0.5) #Se grafica la cantidad de cada recurso que se debe utilizar para el cultivo TSA
for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor de la cantidad de cada recurso que se debe utilizar para el cultivo TSA
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Cantidad de cada recurso que se debe utilizar para el cultivo TSA") #Se coloca el titulo
plt.xlabel("Recurso") #Se coloca el nombre del eje x
plt.ylabel("Cantidad (kg)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los recursos para que no se superpongan
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica

#Grafica de el cultivo MRS
heights = [x["MRS"][r].varValue for r in recursos] #Se obtiene la cantidad de cada recurso que se debe utilizar para el cultivo MRS
bars = plt.bar(recursos, heights, color="green", label="MRS", alpha=0.5) #Se grafica la cantidad de cada recurso que se debe utilizar para el cultivo MRS
for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor de la cantidad de cada recurso que se debe utilizar para el cultivo MRS
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Cantidad de cada recurso que se debe utilizar para el cultivo MRS") #Se coloca el titulo
plt.xlabel("Recurso") #Se coloca el nombre del eje x
plt.ylabel("Cantidad (kg)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los recursos para que no se superpongan
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica

#Grafica de el cultivo SDA
heights = [x["SDA"][r].varValue for r in recursos] #Se obtiene la cantidad de cada recurso que se debe utilizar para el cultivo SDA
bars = plt.bar(recursos, heights, color="orange", label="SDA", alpha=0.5) #Se grafica la cantidad de cada recurso que se debe utilizar para el cultivo SDA
for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor de la cantidad de cada recurso que se debe utilizar para el cultivo SDA
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Cantidad de cada recurso que se debe utilizar para el cultivo SDA") #Se coloca el titulo
plt.xlabel("Recurso") #Se coloca el nombre del eje x
plt.ylabel("Cantidad (kg)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los recursos para que no se superpongan
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica

#Grafica de nutrientes para cada cultivo

#Grafica de nutrientes para el cultivo LB

heights = [pl.value(pl.lpSum([(x["LB"][r].varValue * composicion[r][n]) for r in recursos]) / total_mezcla) for n in nutrientes] #Se obtiene el porcentaje de cada nutriente en la mezcla final para el cultivo LB
bars = plt.bar(nutrientes, heights, color="blue", label="LB", alpha=0.5) #Se grafica el porcentaje de cada nutriente en la mezcla final para el cultivo LB

for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor del porcentaje de cada nutriente en la mezcla final para el cultivo LB
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Porcentaje de cada nutriente en la mezcla final para el cultivo LB") #Se coloca el titulo
plt.xlabel("Nutriente") #Se coloca el nombre del eje x
plt.ylabel("Porcentaje (%)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los nutrientes para que no se superpongan
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica

#Grafica de nutrientes para el cultivo TSA

heights = [pl.value(pl.lpSum([(x["TSA"][r].varValue * composicion[r][n]) for r in recursos]) / total_mezcla) for n in nutrientes] #Se obtiene el porcentaje de cada nutriente en la mezcla final para el cultivo TSA
bars = plt.bar(nutrientes, heights, color="red", label="TSA", alpha=0.5) #Se grafica el porcentaje de cada nutriente en la mezcla final para el cultivo TSA

for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor del porcentaje de cada nutriente en la mezcla final para el cultivo TSA
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Porcentaje de cada nutriente en la mezcla final para el cultivo TSA") #Se coloca el titulo
plt.xlabel("Nutriente") #Se coloca el nombre del eje x
plt.ylabel("Porcentaje (%)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los nutrientes para que no se superpongan
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica

#Grafica de nutrientes para el cultivo MRS

heights = [pl.value(pl.lpSum([(x["MRS"][r].varValue * composicion[r][n]) for r in recursos]) / total_mezcla) for n in nutrientes] #Se obtiene el porcentaje de cada nutriente en la mezcla final para el cultivo MRS
bars = plt.bar(nutrientes, heights, color="green", label="MRS", alpha=0.5) #Se grafica el porcentaje de cada nutriente en la mezcla final para el cultivo MRS

for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor del porcentaje de cada nutriente en la mezcla final para el cultivo MRS
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Porcentaje de cada nutriente en la mezcla final para el cultivo MRS") #Se coloca el titulo
plt.xlabel("Nutriente") #Se coloca el nombre del eje x
plt.ylabel("Porcentaje (%)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los nutrientes para que no se superpongan
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica

#Grafica de nutrientes para el cultivo SDA

heights = [pl.value(pl.lpSum([(x["SDA"][r].varValue * composicion[r][n]) for r in recursos]) / total_mezcla) for n in nutrientes] #Se obtiene el porcentaje de cada nutriente en la mezcla final para el cultivo SDA
bars = plt.bar(nutrientes, heights, color="orange", label="SDA", alpha=0.5) #Se grafica el porcentaje de cada nutriente en la mezcla final para el cultivo SDA

for bar, height in zip(bars, heights):
    plt.text(bar.get_x() + bar.get_width() / 2, height, round(height,2), ha='center', va='bottom') #Se coloca el valor del porcentaje de cada nutriente en la mezcla final para el cultivo SDA
plt.subplots_adjust(bottom=0.3) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.title("Porcentaje de cada nutriente en la mezcla final para el cultivo SDA") #Se coloca el titulo
plt.xlabel("Nutriente") #Se coloca el nombre del eje x
plt.ylabel("Porcentaje (%)") #Se coloca el nombre del eje y
plt.xticks(rotation=35) #Se rota el nombre de los nutrientes para que no se superpongan
plt.ylim(0,max(heights)*1.2) #Se ajusta el espacio para que no se superpongan las etiquetas
plt.show() #Se muestra la grafica



