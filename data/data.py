import numpy as np 
import googlemaps
from datetime import datetime
import pickle



#------------------------------------------------------------------------#
#----------------------------------INFO----------------------------------#
#------------------------------------------------------------------------#

'''
This file is the combined data file containing all the carriers data in one single file.
Also this file contains the already calculated R_k values from all different carriers.
'''



#------------------------------------------------------------------------#
#------------------------------General Data------------------------------#
#------------------------------------------------------------------------#

p_amount = 4 #Amount of Periods
carriers = ['Carrier_1', 'Carrier_2', 'Carrier_3'] #List of carriers
customers = ['Customer_1', 'Customer_2', 'Customer_3', 'Customer_4',
             'Customer_5', 'Customer_6', 'Customer_7', 'Customer_8',
             'Customer_9', 'Customer_10'] #List of customers
depots = ['Depot_1', 'Depot_2', 'Depot_3'] #List of depots
periods = [i for i in range (p_amount + 1) if i != 0] #List of periods
nodes = depots + customers #List of all nodes (including depots and customers)

#Google Data
api_key = 'AIzaSyAdpLMrS2HtCR1gJE2I-ANaZ9qdAv5t8QU'
gmaps = googlemaps.Client(key=api_key)



#------------------------------------------------------------------------#
#-----------------------------Creating Sets------------------------------#
#------------------------------------------------------------------------#

#Set of customers K with each carrier
customers_k = {
    carriers[0]:[customers[0], customers[3], customers[6], customers[8]],
    carriers[1]:[customers[1], customers[4], customers[9]],
    carriers[2]:[customers[2], customers[5], customers[7]]
}

#Set of depots associated with each carrier K
depots_k = {
    carriers[0]: depots[0],
    carriers[1]: depots[1],
    carriers[2]: depots[2]
}

#Identical vehicles of carrier K
vehicles_k = {
    carriers[0]: 3, 
    carriers[1]: 2,
    carriers[2]: 3
}

#Maximum capacity of each carrier K 
Q_max_k = {
    carriers[0]: 600, 
    carriers[1]: 500,
    carriers[2]: 600
}

#Service time for a vehicle to complete service at customer I in period p
#Min: 5 - Max: 100
service_time = {
    depots[0]: {p: 0 for p in periods},
    depots[1]: {p: 0 for p in periods},
    depots[2]: {p: 0 for p in periods},
    customers[0]:  {1: 10,  2: 45,  3: 25,  4: 15},
    customers[1]:  {1: 5,   2: 30,  3: 25,  4: 15}, 
    customers[2]:  {1: 20,  2: 10,  3: 45,  4: 10}, 
    customers[3]:  {1: 35,  2: 15,  3: 40,  4: 10}, 
    customers[4]:  {1: 45,  2: 20,  3: 20,  4: 15}, 
    customers[5]:  {1: 70,  2: 35,  3: 10,  4: 15}, 
    customers[6]:  {1: 30,  2: 40,  3: 30,  4: 10}, 
    customers[7]:  {1: 25,  2: 45,  3: 45,  4: 15}, 
    customers[8]:  {1: 20,  2: 50,  3: 35,  4: 10}, 
    customers[9]:  {1: 15,  2: 5,   3: 45,  4: 30}
}

#Quantity to be delivered to Customer I in Period P
#Min: 30 - 150
quantity_delivered = {
    depots[0]: {p: 0 for p in periods},
    depots[1]: {p: 0 for p in periods},
    depots[2]: {p: 0 for p in periods},
    customers[0]:  {1: 20,  2: 90,  3: 50,  4: 30},
    customers[1]:  {1: 10,  2: 60,  3: 40,  4: 30}, 
    customers[2]:  {1: 45,  2: 25,  3: 90,  4: 20}, 
    customers[3]:  {1: 70,  2: 35,  3: 80,  4: 20}, 
    customers[4]:  {1: 90,  2: 40,  3: 40,  4: 25}, 
    customers[5]:  {1: 140, 2: 70,  3: 25,  4: 30}, 
    customers[6]:  {1: 60,  2: 80,  3: 60,  4: 15}, 
    customers[7]:  {1: 55,  2: 90,  3: 90,  4: 25}, 
    customers[8]:  {1: 40,  2: 100, 3: 70,  4: 15}, 
    customers[9]:  {1: 35,  2: 10,  3: 90,  4: 60},
}

#Revenue from Customer I 
revenue = {
    customers[0]:   40,
    customers[1]:   50,
    customers[2]:   60, 
    customers[3]:   35, 
    customers[4]:   70, 
    customers[5]:   80,  
    customers[6]:   70, 
    customers[7]:   45,   
    customers[8]:   85, 
    customers[9]:   70
}

#Maximum allowed quantity to reduce customer number (alpha)
alpha = {
    carriers[0]: 2,
    carriers[1]: 1,
    carriers[2]: 1
}

#Profit of a carrier if it doesnt participate in a collaboration #NOT FINAL
R_k_simple = {
    carriers[0]: 181, #918 matplot
    carriers[1]: 141, #502
    carriers[2]: 141, #750
    #carriers[3]: 999, #973
}

R_k_live = {
    carriers[0]: 175.9, 
    carriers[1]: 130.81, 
    carriers[2]: 134.88, 
    #carriers[3]: 969, 
}

node_coordinates_1 = {
    depots[0]:      (48.37669963965206, 10.847395818169758), #Phoenix Pharmahandel
    depots[1]:      (48.366202776488905, 10.912264207571434), #Okta Pharma
    depots[2]:      (48.38576430277988, 10.847746195933514), #Betapharm Arzneimittel
    customers[0]:   (48.372238632480766, 10.862015827111975), #Luther King Apotheke
    customers[1]:   (48.36883112692946, 10.893726914208708), #Grottenau Apotheke
    customers[2]:   (48.36488012421214, 10.89395187568196), #Markus Apotheke
    customers[3]:   (48.37717621931016, 10.838580109918029), #Apotheke Via Claudia
    customers[4]:   (48.37894075371622, 10.88154579693216), #Apotheke an der Wertachbrücke
    customers[5]:   (48.36914859303573, 10.888223114642567), #Dr. Kaus Apotheke am Diako
    customers[6]:   (48.36988505176495, 10.904548318918328), #Pelikan Apotheke
    customers[7]:   (48.36118399628752, 10.911567416457691), #Gudjons Apotheke
    customers[8]:   (48.360215616806194, 10.898047745217333), #Bismarck Apotheke
    customers[9]:   (48.36756930024934, 10.848667728295393) #St. Antonius Apotheke
}


#Neue Koordinaten zum testen 
node_coordinates = {
    depots[0]:      (48.381349031151075, 10.875335320909437),   #Betapharm (von den Koordinaten her Oberhausen Bhf. Apotheke)
    depots[1]:      (48.366202776488905, 10.912264207571434),   #Okta Pharma
    depots[2]:      (48.37664980094921, 10.84763538182512),     #Phoenix
    customers[0]:   (48.372725678347464, 10.851883823725666),   #Luther King Apotheke
    customers[1]:   (48.362680437831756, 10.868071860832345),   #Linden Apotheke
    customers[2]:   (48.38064954541611, 10.853754414457114),    #Stefan Apotheke Manhart
    customers[3]:   (48.3747990060179, 10.903667415418784),     #Apotheke am Vincentium
    customers[4]:   (48.386255681437625, 10.847253141222609),   #Apotheke am Oberhausen Bhf (eigentlich Betapharm Koords)
    customers[5]:   (48.36914859303573, 10.888223114642567),    #Dr. Kaus Apotheke am Diako
    customers[6]:   (48.36988505176495, 10.904548318918328),    #Pelikan Apotheke
    customers[7]:   (48.37849049605951, 10.91394362149913),     #Bavaria Apotheke
    customers[8]:   (48.36887051624558, 10.893702098585257),    #Grottenau Apotheke
    customers[9]:   (48.367820748905615, 10.84845144855721)     #St. Antonius Apotheke
}



#------------------------------------------------------------------------#
#----------------------------Assigning Values----------------------------#
#------------------------------------------------------------------------#

#Maximum capacity if all the carriers
Q_max = max(Q_max_k.values())

#Maximum Duration for each Vehicle
T_max = 450

#Maximum time units difference
delta = 70



#------------------------------------------------------------------------#
#---------------------Calculate Matplotlib Values------------------------#
#------------------------------------------------------------------------#

duration_plt = {(i,j): np.hypot(node_coordinates[i][0] - node_coordinates[j][0], node_coordinates[i][1] - node_coordinates[j][1]) * 100 
                for i in nodes for j in nodes}
cost_plt = {(i,j): duration_plt[i,j] * 0.8 
            for i in nodes for j in nodes}

#Testing:
#print("Duration Points: \n", duration_points)
#print("\n\nCost Matrix: \n", cost_points)

#------------------------------------------------------------------------#
#----------------------Calculate Google Values---------------------------#
#------------------------------------------------------------------------#

#Calculate the travel durations
def calculate_duration(origin, destination):
    now = datetime.now()
    directions_result = gmaps.directions(origin, destination, mode="driving", departure_time=now)
    duration_in_traffic = directions_result[0]['legs'][0]['duration_in_traffic']['value']
    return duration_in_traffic / 60 #turn seconds to minutes

#Calculate the real distances in meters
def calculate_distances(origin, destination):
    result = gmaps.distance_matrix(
        origins=origin,
        destinations=destination,
        mode="driving",
        units="metric"
    )
    #Extract distances from API Response
    distance = result["rows"][0]["elements"][0]["distance"]["value"]
    return distance / 1000 #to put it more in relation

#Calculate realistics costs based on differents aspects
def calculate_costs(duration, distance, worker_payment_rate, fuel_price_per_liter, fuel_efficiency):
    """
    Calculate total costs based on travel duration, distance, and other parameters.

    Parameters:
    - duration (float): Travel duration in hours.
    - distance (float): Travel distance in kilometers.
    - worker_payment_rate (float): Payment rate per hour for the worker.
    - fuel_price_per_liter (float): Fuel price per liter.
    - fuel_efficiency (float): Fuel efficiency of the vehicle in kilometers per liter.

    Returns:
    - float: Total cost of the trip.
    """
    worker_payment = duration * worker_payment_rate
    fuel_consumption = distance / fuel_efficiency
    fuel_cost = fuel_consumption * fuel_price_per_liter
    total_cost = worker_payment + fuel_cost

    return total_cost

'''NORMAL PROGRAM'''
#Reading values to improve performance
def load_file(file):
    with open(file, 'rb') as fp:
        data = pickle.load(fp)
    return data
duration_coordinates = load_file('data/duration_c.p')
distance_coordinates = load_file('data/distance_c.p')
cost_coordinates = load_file('data/cost_c.p')


'''
#FIRST TIME EXECUTION
#Assigning all values the first time (when recalculating) GETTING LIVE TRAFFIC DATA AT THE MOMENT
duration_coordinates = {(i,j): calculate_duration(origin=node_coordinates[i], destination=node_coordinates[j]) for i in nodes for j in nodes}
distance_coordinates = {(i,j): calculate_distances(origin=node_coordinates[i], destination=node_coordinates[j]) for i in nodes for j in nodes}
cost_coordinates = {(i,j): calculate_costs(duration=duration_coordinates[i,j],
                                           distance=distance_coordinates[i,j],
                                           worker_payment_rate=20/60,
                                           fuel_price_per_liter=1.9,
                                           fuel_efficiency=10)
                    for i in nodes for j in nodes}

#Saving values in csv files to improve performance
def save_file(name, file):
    with open(name, 'wb') as fp: 
        pickle.dump(file, fp, protocol=pickle.HIGHEST_PROTOCOL)
save_file('duration_c.p', file=duration_coordinates)
save_file('distance_c.p', file=distance_coordinates)
save_file('cost_c.p', file=cost_coordinates)
'''
'''
#Testing
print("\n\n\n\nKosten Daten (live):")
print(cost_coordinates)
print("\n\n\n\nZeit Daten (live):")
print(duration_coordinates)
print("\n\n\n\nDistanz Daten (live):")
print(distance_coordinates)
print("\n\n\n\nKosten Daten (plot):")
print(cost_plt)
print("\n\n\n\n Zeit Daten (plot):")
print(duration_plt)'''