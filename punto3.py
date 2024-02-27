
import pulp as pl
import matplotlib.pyplot as plt
"""Biocultivos es una reconocida empresa que se dedica a la
producción de medios de cultivo para el crecimiento de
microorganismos. Un medio de cultivo es una mezcla de
nutrientes que proporciona un ambiente adecuado para que
microorganismos crezcan y se desarrollen. Estos medios son
esenciales para la investigación científica y el control de calidad
en la industria de alimentos y farmacéutica.
Actualmente, la empresa se encuentra planificando la composición de cuatro (4) medios de
cultivo: Luria-Bertani (LB), Tripticaseína Soya Agar (TSA), Man-Rogosa-Sharpe (MRS) y
Sabouraud Dextrosa Agar (SDA) a partir de cinco (5) nutrientes principales: Agar, Levadura,
Peptona, Cloruro de sodio (NaCl) y Fosfato. En la Tabla 1 se encuentran las proporciones
mínimas y máximas de cada nutriente que debe tener cada uno de los medios de cultivo.
Por ejemplo, el medio de cultivo LB no puede contener Fosfato, mientras que su
requerimiento mínimo y máximo de Agar es de 8.4% y 19%, respectivamente.
Tabla 1. Requerimientos de cada nutriente para cada medio de cultivo.
Medio de
cultivo Requerimiento
Nutriente (%)
Agar Levadura Peptona NaCl Fosfato
LB
Mínimo 8.4 1.26 10.22 3 0
Máximo 19 22.8 36 10 0
TSA
Mínimo 4.33 1.42 5.3 1.26 0
Máximo 26.1 15.4 46 10 0
MRS
Mínimo 1.2 0 0.8 0.025 0.8
Máximo 11 0 11.4 1 72
SDA
Mínimo 0 0 0.5 0 0
Máximo 25 0 74 0 0
Los medios de cultivo se obtienen al mezclar diferentes tipos de recursos. En la Tabla 2 se
encuentra la disponibilidad de cada uno de los recursos, su composición y el costo por
kilogramo. 
Tabla 2. Disponibilidad, composición y costo de cada recurso.
Recurso
Composición (%) Disponible
(kg)
Costo
($/kg)
Agar Levadura Peptona NaCl Fosfato
Fosfato 0 0 0 0 100 206 323
Péptidos 0 0 70 0 0 641 510
Aminoácidos 0 0 48 0 52 120 119
Extracto de
Levadura 0 76 0 13 0 145 340
Agar 84 0 0 5 0 189 826
No hay pérdidas durante el proceso de mezcla de los recursos. Esto quiere decir que, al
emplear un kilogramo de cualquiera de los recursos, se obtendrá un kilogramo del medio
de cultivo para el cual se destine. Por ejemplo, si se usa 1 kilogramo de Péptidos para
producir el medio de cultivo MRS, se obtendrá un kilogramo de MSR. En este ejemplo, el
kilogramo de MSR tendrá: 700 gramos de Peptona. Los restantes 300 gramosson materiales
residuales sin valor nutritivo para el medio de cultivo, que sólo aporta masa al medio de
cultivo, pero no a la participación de nutrientes de interés.
BioCultivos lo ha contratado a usted, persona experta en optimización, para determinar la
composición de cada medio de cultivo, con el objetivo de producir exactamente 300 kg de
cada uno de ellos al menor costo posible. """

import pulp as pl

# Conjuntos
cultivos = ["LB", "TSA", "MRS", "SDA"] 
nutrientes = ["Agar", "Levadura", "Peptona", "NaCl", "Fosfato"]
recursos = ["Fosfato", "Péptidos", "Aminoácidos", "Extracto de Levadura", "Agar"]

# Parámetros
minimo = {"LB": {"Agar": 8.4, "Levadura": 1.26, "Peptona": 10.22, "NaCl": 3, "Fosfato": 0},
          "TSA": {"Agar": 4.33, "Levadura": 1.42, "Peptona": 5.3, "NaCl": 1.26, "Fosfato": 0},
          "MRS": {"Agar": 1.2, "Levadura": 0, "Peptona": 0.8, "NaCl": 0.025, "Fosfato": 0.8},
          "SDA": {"Agar": 0, "Levadura": 0, "Peptona": 0.5, "NaCl": 0, "Fosfato": 0}}

maximo = {"LB": {"Agar": 19, "Levadura": 22.8, "Peptona": 36, "NaCl": 10, "Fosfato": 0},
          "TSA": {"Agar": 26.1, "Levadura": 15.4, "Peptona": 46, "NaCl": 10, "Fosfato": 0},
          "MRS": {"Agar": 11, "Levadura": 0, "Peptona": 11.4, "NaCl": 1, "Fosfato": 72},
          "SDA": {"Agar": 25, "Levadura": 0, "Peptona": 74, "NaCl": 0, "Fosfato": 0}}

disponibilidad = {"Fosfato": 206, "Péptidos": 641, "Aminoácidos": 120, 
                 "Extracto de Levadura": 145, "Agar": 189}

costo = {"Fosfato": 323, "Péptidos": 510, "Aminoácidos": 119, 
         "Extracto de Levadura": 340, "Agar": 826}

composicion = {"Fosfato": {"Agar": 0, "Levadura": 0, "Peptona": 0, "NaCl": 0, "Fosfato": 100},
               "Péptidos": {"Agar": 0, "Levadura": 0, "Peptona": 70, "NaCl": 0, "Fosfato": 0},
               "Aminoácidos": {"Agar": 0, "Levadura": 0, "Peptona": 48, "NaCl": 0, "Fosfato": 52},
               "Extracto de Levadura": {"Agar": 0, "Levadura": 76, "Peptona": 0, "NaCl": 13, "Fosfato": 0},
               "Agar": {"Agar": 84, "Levadura": 0, "Peptona": 0, "NaCl": 5, "Fosfato": 0}}

modelo = pl.LpProblem("Minimizar", pl.LpMinimize)

# Variables
x = pl.LpVariable.dicts("x", (cultivos, recursos), lowBound=0, cat="Continuous")

# Función objetivo
modelo += pl.lpSum([x[c][r] * costo[r] for c in cultivos for r in recursos])

#Restricciones

#Disponibilidad de recursos
for r in recursos:
    modelo += pl.lpSum([x[c][r] for c in cultivos]) <= disponibilidad[r]
    
#Produccion total de cada cultivo
for c in cultivos:
    modelo += pl.lpSum([x[c][r] for r in recursos]) == 300

#Restricciones de nutrientes

#Imprimir
modelo.solve()
print(pl.LpStatus[modelo.status])
for c in cultivos:
    for r in recursos:
        print(c, r, x[c][r].varValue)
print("Costo total: ", pl.value(modelo.objective))

#gdfgdf
###