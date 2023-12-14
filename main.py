from gurobi import Model, GRB, quicksum
import numpy as np
import matplotlib.pyplot as plt
import googlemaps
from data.data import *
import folium



#------------------------------------------------------------------------#
#----------------------------------INFO----------------------------------#
#------------------------------------------------------------------------#

'''
This file is for calculating the nocollaboration profits of each carrier. 
For this I have created several different data files - only including their respective data.
'''



#------------------------------------------------------------------------#
#------------------------------General Data------------------------------#
#------------------------------------------------------------------------#

#Initialize Google Client with valid API key
api_key = 'AIzaSyAdpLMrS2HtCR1gJE2I-ANaZ9qdAv5t8QU'
gmaps = googlemaps.Client(key=api_key)



#------------------------------------------------------------------------#
#--------------------------Simplified or LIVE----------------------------#
#------------------------------------------------------------------------#

#Use simplified data
#duration = duration_plt
#cost = cost_plt
#R_k = R_k_simple

#Use real data
duration = duration_coordinates 
cost = cost_coordinates
R_k = R_k_live



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

#--17--#
model.addConstrs(quicksum(revenue[j]*Y[j,k] for j in customers) - quicksum(cost[i,j] * X[i,j,k,p] for p in periods for i in nodes for j in customers) >= R_k[k]
                 for k in carriers)

#--18--#
model.addConstrs(quicksum(Y[j,k] for j in customers) >= len(customers_k[k]) - alpha[k] 
                 for k in carriers)

#-------------------------Valid Inequalities-----------------------------#

#--19--#
model.addConstrs(V[k,p] >= quicksum((quantity_delivered[i][p]*Y[i,k])/Q_max_k[k] for i in customers)
                 for k in carriers for p in periods)

#--20--#
model.addConstrs(quicksum(revenue[i]*Y[i,k] for i in customers) >= R_k[k]
                 for k in carriers)

#--21--#
model.addConstrs(quicksum(quantity_delivered[i][p]*Y[i,k] for i in customers) <= vehicles_k[k]*Q_max_k[k]
                 for k in carriers for p in periods)


'''
Potenziell noch lauslöschen die Valid Inequalities die eh nicht klappne
#--22--#
#model.addConstrs(quicksum)

#--23--#
model.addConstrs(quicksum(Y[i,k] + V[k,p] for i in customers if quantity_delivered[i][p] > 0) <= quicksum(X[i,j,k,p] for i in nodes for j in nodes)
                 for k in carriers for p in periods)

#--24--# (second part of 23)
model.addConstrs(quicksum(X[i,j,k,p] for i in nodes for j in nodes) <= quicksum(Y[i,k] + vehicles_k[k] for i in customers if quantity_delivered[i][p] > 0)
                 for k in carriers for p in periods)
'''
#------------------------------------------------------------------------#
#------------------------Model Optimization------------------------------#
#------------------------------------------------------------------------#

model.optimize()

#---------------------Printing the Carrier Profits-----------------------#

for k in carriers:
    # Berechnung des Gewinns für den aktuellen Carrier
    carrier_profit = sum(revenue[j] * Y[j, k].x for j in customers) - sum(cost[i, j] * X[i, j, k, p].x for p in periods for i in nodes for j in customers)

    # Ausgabe des Gewinns für den aktuellen Carrier
    print(f"Gewinn für {k}: {carrier_profit:.2f}")

#-----------------------Printing the Variables---------------------------#

print("Objective Value: " ,str(round(model.ObjVal, 2)))
for v in model.getVars():
    if v.x > 0.9: 
        print(str(v.VarName)+"="+str(v.x))



#------------------------------------------------------------------------#
#---------------------Graphical Illustration-----------------------------#
#------------------------------------------------------------------------#

#----------------------Matplotlib Optimal Routes-------------------------#

def plot_opt_routes():
    # Create color map for the depots
    depots_colors = {depot: f"C{i}" for i, depot in enumerate(depots)}

    # Create color map for the customers
    customers_colors = {customer: f"C{i}" for i, customer in enumerate(customers_k)}

    # Set a larger figure size
    plt.figure(figsize=(12, 10))

    # Create a scatter plot of depots and customers
    for node, coords in node_coordinates.items():
        if node in depots:
            plt.scatter(coords[1], coords[0], label=node, marker="D", s=100, color=depots_colors[node], alpha=0.8)
            plt.annotate(f'{node}\n(T: 0)', (coords[1], coords[0]), textcoords="offset points", xytext=(6, 6), ha='right', fontsize=9, color='black')
        elif node in customers:
            k = [k for k, v in customers_k.items() if node in v][0]  # find the carrier for the customers
            plt.scatter(coords[1], coords[0], label=node, marker="o", s=80, color=customers_colors[k], alpha=0.8)
            #Annotating for better visibility
            arrival_time = T[node, 1].x  # Adjust the period as needed
            plt.annotate(f'{node}\n(T: {arrival_time:.1f})', (coords[1], coords[0]), textcoords="offset points", xytext=(6, 6), ha='right', fontsize=9, color='black')

    # Plot the routes
    for k in carriers:
        carrier_label_added = False
        for i, j, t, p in i_j_k_p:
            if X[i, j, k, p].x > 0.9:
                route_x = [node_coordinates[i][1], node_coordinates[j][1]]
                route_y = [node_coordinates[i][0], node_coordinates[j][0]]

                # Plot the route with the corresponding color and line style
                if not carrier_label_added:
                    plt.plot(route_x, route_y, label=f"{k}", color=customers_colors[k], linewidth=2.2, linestyle='-', alpha=0.7)
                    carrier_label_added = True
                else:
                    plt.plot(route_x, route_y, color=customers_colors[k], linewidth=2.2, linestyle='-', alpha=0.7)

    # Set labels and legend
    plt.title("Optimierte Routen der Anbieter durch Kollaborationen")
    plt.xlabel("Längengrad")
    plt.ylabel("Breitengrad")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Nodes", title_fontsize='12', fontsize='10')  # Place legend outside the plot
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

#-----------------------Google Maps Visualization------------------------#

# Define colors for each carrier
carrier_colors = {
    "Anbieter 1": 'blue',
    "Anbieter 2": 'red',
    "Anbieter 3": 'green',
}

def get_detailed_routes():
    gmaps = googlemaps.Client(key=api_key)

    detailed_routes = []
    for carrier in carriers:
        route_coords = []

        for i, j, _, _ in i_j_k_p:
            if X[i, j, carrier, 1].x > 0.9:
                route_coords.append(node_coordinates[i])

        # Append the depot to the route
        depot_coord = node_coordinates[depots_k[carrier]]
        route_coords.append(depot_coord)

        # Split waypoints into chunks of 25 (because of API Limitations)
        waypoint_chunks = [route_coords[i:i + 25] for i in range(0, len(route_coords), 25)]

        # Initialize the full route
        full_route = []

        # Request detailed route for each chunk
        for waypoints in waypoint_chunks:
            # Request detailed route from Google Maps API with adjustments
            directions_result = gmaps.directions(
                waypoints[0],
                waypoints[-1],
                waypoints=waypoints[1:-1],
                mode="driving",
                avoid="ferries"
            )

            # Extract detailed route coordinates
            route = [(step['start_location']['lat'], step['start_location']['lng']) for leg in directions_result[0]['legs'] for step in leg['steps']]
            full_route.extend(route)

        detailed_routes.append(full_route)

    return detailed_routes

def create_map_with_markers_and_routes():
    # Create a Folium map centered around the first depot
    map_routes = folium.Map(location=[node_coordinates[depots[0]][0], node_coordinates[depots[0]][1]], zoom_start=12)

    # Add markers for depots with carrier-specific colors
    for carrier, depot in depots_k.items():
        folium.Marker(
            location=[node_coordinates[depot][0], node_coordinates[depot][1]],
            popup=f'{depot} ({carrier})',
            icon=folium.Icon(color=carrier_colors[carrier], icon='glyphicon-home')
        ).add_to(map_routes)

        # Add label next to the marker
        folium.map.Marker(
            [node_coordinates[depot][0], node_coordinates[depot][1]],
            icon=folium.DivIcon(
                icon_size=(150, 36),
                icon_anchor=(7, 15),
                html=f'<div style="font-size: 10pt; color : {carrier_colors[carrier]};">{depot}</div>'
            )
        ).add_to(map_routes)

    # Add markers for customers with carrier-specific colors
    for carrier, customer_list in customers_k.items():
        for customer in customer_list:
            folium.Marker(
                location=[node_coordinates[customer][0], node_coordinates[customer][1]],
                popup=f'{customer} ({carrier})',
                icon=folium.Icon(color=carrier_colors[carrier], icon='glyphicon-user', prefix='glyphicon')
            ).add_to(map_routes)

            # Add label next to the marker
            folium.map.Marker(
                [node_coordinates[customer][0], node_coordinates[customer][1]],
                icon=folium.DivIcon(
                    icon_size=(150, 36),
                    icon_anchor=(7, 15),
                    html=f'<div style="font-size: 10pt; color : {carrier_colors[carrier]};">{customer}</div>'
                )
            ).add_to(map_routes)

    # Add detailed routes to the map
    detailed_routes = get_detailed_routes()
    for carrier, route in zip(carriers, detailed_routes):
        folium.PolyLine(route, color=carrier_colors[carrier], weight=5, opacity=1).add_to(map_routes)

    # Create a legend (workaround using HTML)
    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 50px; z-index:1000; font-size: 12pt; background-color: white; padding: 10px; border: 1px solid grey;">
        <p><strong>Legend</strong></p>
        <p><i class="glyphicon glyphicon-home" style="color: blue;"></i> Anbieter 1</p>
        <p><i class="glyphicon glyphicon-home" style="color: red;"></i> Anbieter 2</p>
        <p><i class="glyphicon glyphicon-home" style="color: green;"></i> Anbieter 3</p>
        <!-- Add more entries for each carrier -->
    </div>
    """

    map_routes.get_root().html.add_child(folium.Element(legend_html))

    map_routes.save('map_with_markers_and_routes.html')

#-----------------------Executing the Visualization----------------------#

#Google Maps:
#create_map_with_markers_and_routes()

#Matplotlib:
plot_opt_routes()