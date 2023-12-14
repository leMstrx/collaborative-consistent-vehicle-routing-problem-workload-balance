import matplotlib.pyplot as plt
from data.data import *

#------------------------------------------------------------------------#
#---------Plotting no Collaborations Routes with all Carriers------------#
#------------------------------------------------------------------------#

merged_list = {
    #Carrier 1
    ('Depot 1', 'Kunde 1', 'Anbieter 1', 2): 1.0,
    ('Depot 1', 'Kunde 7', 'Anbieter 1', 1): 1.0,
    ('Depot 1', 'Kunde 7', 'Anbieter 1', 2): 1.0,
    ('Depot 1', 'Kunde 7', 'Anbieter 1', 3): 1.0,
    ('Depot 1', 'Kunde 7', 'Anbieter 1', 4): 1.0,
    ('Kunde 1', 'Kunde 4', 'Anbieter 1', 1): 1.0,
    ('Kunde 1', 'Kunde 4', 'Anbieter 1', 2): 1.0,
    ('Kunde 1', 'Kunde 4', 'Anbieter 1', 3): 1.0,
    ('Kunde 1', 'Kunde 4', 'Anbieter 1', 4): 1.0,
    ('Kunde 4', 'Depot 1', 'Anbieter 1', 1): 1.0,
    ('Kunde 4', 'Depot 1', 'Anbieter 1', 2): 1.0,
    ('Kunde 4', 'Depot 1', 'Anbieter 1', 3): 1.0,
    ('Kunde 4', 'Depot 1', 'Anbieter 1', 4): 1.0,
    ('Kunde 7', 'Kunde 9', 'Anbieter 1', 1): 1.0,
    ('Kunde 7', 'Kunde 9', 'Anbieter 1', 2): 1.0,
    ('Kunde 7', 'Kunde 9', 'Anbieter 1', 3): 1.0,
    ('Kunde 7', 'Kunde 9', 'Anbieter 1', 4): 1.0,
    ('Kunde 9', 'Depot 1', 'Anbieter 1', 2): 1.0,
    ('Kunde 9', 'Kunde 1', 'Anbieter 1', 1): 1.0,
    ('Kunde 9', 'Kunde 1', 'Anbieter 1', 3): 1.0,
    ('Kunde 9', 'Kunde 1', 'Anbieter 1', 4): 1.0,
    #Carrier 2
    ('Depot 2', 'Kunde 5', 'Anbieter 2', 1): 1.0,
    ('Depot 2', 'Kunde 5', 'Anbieter 2', 2): 1.0,
    ('Depot 2', 'Kunde 5', 'Anbieter 2', 3): 1.0,
    ('Depot 2', 'Kunde 5', 'Anbieter 2', 4): 1.0,
    ('Kunde 2', 'Depot 2', 'Anbieter 2', 1): 1.0,
    ('Kunde 2', 'Depot 2', 'Anbieter 2', 2): 1.0,
    ('Kunde 2', 'Depot 2', 'Anbieter 2', 3): 1.0,
    ('Kunde 2', 'Depot 2', 'Anbieter 2', 4): 1.0,
    ('Kunde 5', 'Kunde 10', 'Anbieter 2',1): 1.0,
    ('Kunde 5', 'Kunde 10', 'Anbieter 2',2): 1.0,
    ('Kunde 5', 'Kunde 10', 'Anbieter 2',3): 1.0,
    ('Kunde 5', 'Kunde 10', 'Anbieter 2',4): 1.0,
    ('Kunde 10', 'Kunde 2', 'Anbieter 2',1): 1.0,
    ('Kunde 10', 'Kunde 2', 'Anbieter 2',2): 1.0,
    ('Kunde 10', 'Kunde 2', 'Anbieter 2',3): 1.0,
    ('Kunde 10', 'Kunde 2', 'Anbieter 2',4): 1.0,
    #Carrier 3
    ('Depot 3', 'Kunde 3', 'Anbieter 3', 1): 1.0,
    ('Depot 3', 'Kunde 3', 'Anbieter 3', 2): 1.0,
    ('Depot 3', 'Kunde 3', 'Anbieter 3', 3): 1.0,
    ('Depot 3', 'Kunde 3', 'Anbieter 3', 4): 1.0,
    ('Kunde 3', 'Kunde 8', 'Anbieter 3', 1): 1.0,
    ('Kunde 3', 'Kunde 8', 'Anbieter 3', 2): 1.0,
    ('Kunde 3', 'Kunde 8', 'Anbieter 3', 3): 1.0,
    ('Kunde 3', 'Kunde 8', 'Anbieter 3', 4): 1.0,
    ('Kunde 6', 'Depot 3', 'Anbieter 3', 1): 1.0,
    ('Kunde 6', 'Depot 3', 'Anbieter 3', 2): 1.0,
    ('Kunde 6', 'Depot 3', 'Anbieter 3', 3): 1.0,
    ('Kunde 6', 'Depot 3', 'Anbieter 3', 4): 1.0,
    ('Kunde 8', 'Kunde 6', 'Anbieter 3', 1): 1.0,
    ('Kunde 8', 'Kunde 6', 'Anbieter 3', 2): 1.0,
    ('Kunde 8', 'Kunde 6', 'Anbieter 3', 3): 1.0,
    ('Kunde 8', 'Kunde 6', 'Anbieter 3', 4): 1.0,
}

all_tuples = []

#Generate all possible tuples for decision variables
i_j_k_p = [(i,j,k,p) for i in nodes for j in nodes for k in carriers for p in periods] #Setting up the indeces

for i,j,k,p in i_j_k_p:
    all_tuples.append((i,j,k,p))

print(all_tuples)

print(merged_list)

all_tuples_with_values = {(i, j, k, p): 1.0 if (i, j, k, p) in merged_list else 0.0 for i, j, k, p in all_tuples}

print(all_tuples_with_values)

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
            plt.annotate(node, (coords[1], coords[0]), textcoords="offset points", xytext=(6, 6), ha='right', fontsize=9, color='black')
        elif node in customers:
            k = [k for k, v in customers_k.items() if node in v][0]  # find the carrier for the customers
            plt.scatter(coords[1], coords[0], label=node, marker="o", s=80, color=customers_colors[k], alpha=0.8)
            plt.annotate(node, (coords[1], coords[0]), textcoords="offset points", xytext=(6, 6), ha='right', fontsize=9, color='black')
    
     # Plot the routes with value 1.0
    for k in carriers:
        carrier_label_added = False
        for i, j, t, p in all_tuples_with_values.keys():
            if all_tuples_with_values[i, j, t, p] == 1.0 and t == k:
                route_x = [node_coordinates[i][1], node_coordinates[j][1]]
                route_y = [node_coordinates[i][0], node_coordinates[j][0]]

                # Plot the route with the corresponding color and line style
                if not carrier_label_added:
                    plt.plot(route_x, route_y, label=f"{k}", color=customers_colors[k], linewidth=2.2, linestyle='-', alpha=0.7)
                    carrier_label_added = True
                else:
                    plt.plot(route_x, route_y, color=customers_colors[k], linewidth=2.2, linestyle='-', alpha=0.7)
    
    # Set labels and legend
    plt.title("Routen der Anbieter mit zugeteilten Kunden (ohne Kollaborationen)")
    plt.xlabel("Längengrad")
    plt.ylabel("Breitengrad")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Nodes", title_fontsize='12', fontsize='10')  # Place legend outside the plot
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

plot_opt_routes()