
import matplotlib.pyplot as plt
import pulp as lp

prob= lp.LpProblem("Biocultivos", lp.LpMinimize)
#CONJUNTOS
M = ["LB", "TSA", "MRS", "SDA"]
N = ["ag", "l", "p", "cl", "f"]
R = ["F", "P", "A", "EL", "AG"]

#PARAMETROS

#costos
c = {"F":323,
     "P":510,
     "A":119,
     "EL":340,
     "AG":826}

#disponibilidad
k={"F":206,
     "P":641,
     "A":120,
     "EL":145,
     "AG":189}

#minimos
mi= {("LB","ag"):8.4,
     ("LB","l"):1.26,
     ("LB","p"):10.22,
     ("LB","cl"):3,
     ("LB","f"):0,
     ("TSA","ag"):4.33,
     ("TSA","l"):1.42,
     ("TSA","p"):5.3,
     ("TSA","cl"):1.26,
     ("TSA","f"):0,
     ("MRS","ag"):1.2,
     ("MRS","l"):0,
     ("MRS","p"):0.8,
     ("MRS","cl"):0.025,
     ("MRS","f"):0.8,
     ("SDA","ag"):0,
     ("SDA","l"):0,
     ("SDA","p"):0.5,
     ("SDA","cl"):0,
     ("SDA","f"):0}

#maximos
ma= {("LB","ag"):19,
     ("LB","l"):22.8,
     ("LB","p"):36,
     ("LB","cl"):10,
     ("LB","f"):0,
     ("TSA","ag"):26.1,
     ("TSA","l"):15.4,
     ("TSA","p"):46,
     ("TSA","cl"):10,
     ("TSA","f"):0,
     ("MRS","ag"):11,
     ("MRS","l"):0,
     ("MRS","p"):11.4,
     ("MRS","cl"):1,
     ("MRS","f"):72,
     ("SDA","ag"):25,
     ("SDA","l"):0,
     ("SDA","p"):74,
     ("SDA","cl"):0,
     ("SDA","f"):0}

#demanda
d=300

#proporcionalidad
r= {("F","ag"):0,
     ("F","l"):0,
     ("F","p"):0,
     ("F","cl"):0,
     ("F","f"):100,
     ("P","ag"):0,
     ("P","l"):0,
     ("P","p"):70,
     ("P","cl"):0,
     ("P","f"):0,
     ("A","ag"):0,
     ("A","l"):0,
     ("A","p"):48,
     ("A","cl"):0,
     ("A","f"):52,
     ("EL","ag"):0,
     ("EL","l"):76,
     ("EL","p"):0,
     ("EL","cl"):13,
     ("EL","f"):0,
     ("AG","ag"):84,
     ("AG","l"):0,
     ("AG","p"):0,
     ("AG","cl"):5,
     ("AG","f"):0}

#VARIABLE DE DECISION
x={(j,i):lp.LpVariable(f"{j}{i}",0,None,lp.LpContinuous)for j in R for i in M}


#RESTRICCIONES

#minimos
for i in M:
    for g in N:
        total_nutrientes= lp.lpSum(x[j,i]*(r[j,g]/100) for j in R)
        prob+=total_nutrientes >= (mi[i,g]/100) *d
        prob+=total_nutrientes <= (ma[i,g]/100) * d
        
#cumplir demanda
for i in M:
    prob+= lp.lpSum(x[j,i] for j in R) == d
    
#Naturaleza de la variable
for i in M:
    for j in R:
        x[j,i]>=0
        
#Respetar las disponibilidades de los recursos
for j in R:
    prob+= lp.lpSum(x[j,i] for i in M) <=k[j]
    
#FUNCION OBJETIVO
prob+= lp.lpSum(c[j]*x[j,i] for i in M for j in R)

prob.solve()

print("Status",lp.LpStatus[prob.status])

print(lp.value(prob.objective))

for i in M: 
    print(f"Para el cultivo de {i} se deben usar:")
    for j in R:
        print(f"{round(x[j,i].varValue,2)} KG de {j}")
        
#Graficar


#En un pie chart mostrar los porcentajes de los nutrientes en un pie chart y que sumen 100% teniendo en cuenta los materiales residuales

plt.figure(figsize=(10,10))
for i in M:
    nutrientes= [x[j,i].varValue for j in R]
    plt.pie(nutrientes, labels=R, autopct="%1.1f%%")
    plt.title(f"Nutrientes para el cultivo de {i}")
    plt.show()
    

