import numpy as np 
import googlemaps
from datetime import datetime
import pickle



#------------------------------------------------------------------------#
#----------------------------------INFO----------------------------------#
#------------------------------------------------------------------------#

'''
This file is the carrier_4 specific file containing just the data important for carrier 4..
This file is needed to calculate R_k for carrier_4.
'''



#------------------------------------------------------------------------#
#------------------------------General Data------------------------------#
#------------------------------------------------------------------------#

p_amount = 4 #Amount of Periods
carriers = ['Carrier_4']
customers = ['Customer_4', 'Customer_8', 'Customer_11', 'Customer_13']
depots = ['Depot_4']
periods = [i for i in range(p_amount + 1) if i != 0]
nodes = depots + customers

#Google Data
api_key = 'AIzaSyAdpLMrS2HtCR1gJE2I-ANaZ9qdAv5t8QU'
gmaps = googlemaps.Client(key=api_key)



#------------------------------------------------------------------------#
#-----------------------------Creating Sets------------------------------#
#------------------------------------------------------------------------#

customers_k = {
    carriers[0]: [customers[0], customers[1], customers[2], customers[3]]
}

depots_k = {
    carriers[0]: depots[0]
}

vehicles_k = {
    carriers[0]: 4
}

Q_max_k = {
    carriers[0]: 700
}

service_time = {
    depots[0]: {p: 0 for p in periods},
    customers[0]: {1: 35, 2: 15, 3: 40, 4: 10},
    customers[1]: {1: 25, 2: 45, 3: 45, 4: 15},
    customers[2]: {1: 35, 2: 10, 3: 15, 4: 30},
    customers[3]: {1: 35,  2: 10,  3: 30,  4: 25}
}

quantity_delivered = {
    depots[0]: {p: 0 for p in periods},
    customers[0]: {1: 70, 2: 35, 3: 80, 4: 20},
    customers[1]: {1: 55, 2: 90, 3: 90, 4: 25},
    customers[2]: {1: 75, 2: 25, 3: 30, 4: 65},
    customers[3]: {1: 60,  2: 20,  3: 60,  4: 50}, 
}

revenue = {
    customers[0]: 400,
    customers[1]: 250,
    customers[2]: 250,
    customers[3]: 150
}

alpha = {
    carriers[0]: 3
}

node_coordinates = {
    depots[0]:      (48.38576430277988, 10.847746195933514), #Betapharm Arzneimittel
    customers[0]:   (48.37717621931016, 10.838580109918029), #Apotheke Via Claudia
    customers[1]:   (48.36118399628752, 10.911567416457691), #Gudjons Apotheke
    customers[2]:  (48.37511817959376, 10.895619273203693), #Frauentor Apotheke
    customers[3]:  (48.3625355405014, 10.868040728280596), #Linden Apotheke
    #customers[13]:  (5, 8)
}


#------------------------------------------------------------------------#
#----------------------------Assigning Values----------------------------#
#------------------------------------------------------------------------#

#Maximum capacity if all the carriers
Q_max = max(Q_max_k.values())

#Maximum Duration for each Vehicle
T_max = 250

#Maximum time units difference
delta = 70



#------------------------------------------------------------------------#
#---------------------Calculate Matplotlib Values------------------------#
#------------------------------------------------------------------------#

duration_points = {(i,j): np.hypot(node_coordinates[i][0] - node_coordinates[j][0], node_coordinates[i][1] - node_coordinates[j][1]) * 100
                   for i in nodes for j in nodes}
cost_points = {(i,j): duration_points[i,j] * 0.8
               for i in nodes for j in nodes}



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

'''NORMAL PROGRAM
#Reading values to improve performance
def load_file(file):
    with open(file, 'rb') as fp:
        data = pickle.load(fp)
    return data
duration_coordinates = load_file('carrier_4_duration_c.p')
distance_coordinates = load_file('carrier_4_distance_c.p')
cost_coordinates = load_file('carrier_4_cost_c.p')
'''


#FIRST TIME PROGRAMM
#Assigning all values the first time (when recalculating)
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
save_file('carrier_4_duration_c.p', file=duration_coordinates)
save_file('carrier_4_distance_c.p', file=distance_coordinates)
save_file('carrier_4_cost_c.p', file=cost_coordinates)
