#General Imports 
from gurobi import Model, GRB, quicksum
import numpy as np
import matplotlib.pyplot as plt



#------------------------------------------------------------------------#
#----------------------------------INFO----------------------------------#
#------------------------------------------------------------------------#

'''
This file is for calculating the nocollaboration profits of each carrier. 
For this I have created several different data files - only including their respective data.
'''

#------------------------------------------------------------------------#
#----------------------------Specific Imports----------------------------#
#------------------------------------------------------------------------#

#from data.data import * #Use when plotting everything without collabs


#------------------------------------------------------------------------#
#----------------------------Specific Imports----------------------------#
#------------------------------------------------------------------------#

#from data.carrier_data.carrier_1 import *
#from data.carrier_data.carrier_2 import *
from data.carrier_data.carrier_3 import *



#------------------------------------------------------------------------#
#---------------------Duration / Cost Definition-------------------------#
#------------------------------------------------------------------------#

#Use simplified data
#duration = duration_plt
#cost = cost_plt

#Use live data
duration = duration_coordinates 
cost = cost_coordinates



#------------------------------------------------------------------------#
#------------------------Problem Definition------------------------------#
#------------------------------------------------------------------------#

model = Model('CCVRPWV') #Creating the gurobi model
model.ModelSense = GRB.MAXIMIZE #Set the objective function to maximize

#-------------------------------Indeces----------------------------------#
i_k = [(i,k) for i in customers for k in carriers]
i_j_k_p = [(i,j,k,p) for i in nodes for j in nodes for k in carriers for p in periods]
i_p_n = [(i,p) for i in nodes for p in periods] #nodes
k_p = [(k,p) for k in carriers for p in periods]

#---------------------Decision Variables - Binary------------------------#
Y = model.addVars(i_k, vtype=GRB.BINARY, name='Y')
X = model.addVars(i_j_k_p, vtype=GRB.BINARY, name='X')

#--------------------Decision Variables - Continous----------------------#
T = model.addVars(i_p_n, vtype=GRB.CONTINUOUS, name='T')
L = model.addVars(i_p_n, vtype=GRB.CONTINUOUS, name='L')
V = model.addVars(k_p, vtype=GRB.INTEGER, name='V')



#------------------------------------------------------------------------#
#------------------------Objective Function------------------------------#
#------------------------------------------------------------------------#

#--1--#
model.setObjective(quicksum(revenue[i] for i in customers) - quicksum(cost[i,j] * X[i,j,k,p] for (i,j,k,p) in i_j_k_p))



#------------------------------------------------------------------------#
#-----------------------------Constraints--------------------------------#
#------------------------------------------------------------------------#



#--2--#
model.addConstrs(quicksum(Y[i,k] for k in carriers) == 1 
                 for i in customers)

#--3--#
model.addConstrs(quicksum(X[i,j,k,p] for i in nodes) <= Y[j,k]
                 for j in customers for k in carriers for p in periods)

#--4--#
model.addConstrs(quicksum(X[i,j,k,p] for i in nodes) == quicksum(X[j,i,k,p] for i in nodes) 
                 for j in customers for k in carriers for p in periods)

#--5--#
model.addConstrs(quicksum(X[j,depots_k[k],k,p] for j in customers) <= vehicles_k[k]
                 for k in carriers for p in periods)

#--6--#
model.addConstrs(T[j,p] >= T[i,p] + duration[i,j] + service_time[i][p] - T_max*(1-quicksum(X[i,j,k,p] for k in carriers))
                 for j in customers for i in nodes for p in periods)

#--7--#
model.addConstrs(T[j,p] + duration[i,j] * quicksum(X[j,i,k,p] for k in carriers) <= T_max
                 for j in customers for i in depots for p in periods)

#--8--#
model.addConstrs(L[j,p] >= L[i,p] + quantity_delivered[j][p] - Q_max*(1-quicksum(X[i,j,k,p] for k in carriers)) 
                 for j in customers for i in nodes for p in periods)

#--9--#
model.addConstrs(L[j,p] <= Q_max
                 for j in customers for p in periods)

#--10--#
model.addConstrs(X[i,j,k,p] == 0
                 for j in customers for k in carriers for i in depots if i != depots_k[k] for p in periods)

#--11--#
model.addConstrs(X[j,i,k,p] == 0
                 for j in customers for k in carriers for i in depots if i != depots_k[k] for p in periods)

#--12--#
model.addConstrs(quicksum(X[i,j,k,p] for i in nodes for k in carriers) >= quantity_delivered[j][p]*1/Q_max 
                 for j in customers for p in periods)

#--13--#
model.addConstrs(T[i,p] == 0
                 for i in depots for p in periods)

#--14--#
model.addConstrs(L[i,p] == 0
                 for i in depots for p in periods) 

#--15--# (18)
model.addConstrs(T[j,p1] - T[j,p2] <= delta
                 for j in customers for p1 in periods if quantity_delivered[j][p1] > 0 for p2 in periods if quantity_delivered[j][p2] > 0)

#--16--# (19)
model.addConstrs(T[j,p2] - T[j,p1] <= delta
                 for j in customers for p1 in periods if quantity_delivered[j][p1] > 0 for p2 in periods if quantity_delivered[j][p2] > 0)



#------------------------------------------------------------------------#
#------------------------Model Optimization------------------------------#
#------------------------------------------------------------------------#

model.optimize()

# Extracting and printing the variables
print("Objective Value: ", str(round(model.ObjVal, 2)))

#-----------------------Printing the Variables---------------------------#

print("Objective Value: " ,str(round(model.ObjVal, 2)))
for v in model.getVars():
    if v.x > 0.9: 
        print(str(v.VarName)+"="+str(v.x))


#------------------------------------------------------------------------#
#-----------------------Plotting each Carrier----------------------------#
#------------------------------------------------------------------------#


def plot_single_carrier():
    # Plotting the nodes
    plt.figure()
    plt.title("Nodes - Depot and Customers")

    # Plotting depot
    plt.scatter(node_coordinates[depots_k[carriers[0]]][1], node_coordinates[depots_k[carriers[0]]][0], marker='X', color='blue', label='Depot')

    # Plotting customers
    for i in customers:
        plt.scatter(node_coordinates[i][1], node_coordinates[i][0], marker='o', label=i)

    plt.legend()
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

plot_single_carrier()





