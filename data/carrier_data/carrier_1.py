import numpy as np 
import googlemaps
from datetime import datetime
import pickle



#------------------------------------------------------------------------#
#----------------------------------INFO----------------------------------#
#------------------------------------------------------------------------#

'''
This file is the carrier_1 specific file containing just the data important for carrier 1..
This file is needed to calculate R_k for carrier_1.
'''



#------------------------------------------------------------------------#
#------------------------------General Data------------------------------#
#------------------------------------------------------------------------#

p_amount = 4 #Amount of Periods
carriers = ['Anbieter 1']
customers = ['Kunde 1', 'Kunde 4', 'Kunde 7', 'Kunde 9']
depots = ['Depot 1']
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
    carriers[0]: 3
}

Q_max_k = {
    carriers[0]: 600
}

service_time = {
    depots[0]: {p: 0 for p in periods},
    customers[0]: {1: 10, 2: 45, 3: 25, 4: 15},
    customers[1]: {1: 35, 2: 15, 3: 40, 4: 10},
    customers[2]: {1: 30, 2: 40, 3: 30, 4: 10},
    customers[3]: {1: 20, 2: 50, 3: 35, 4: 10}
}

quantity_delivered = {
    depots[0]: {p: 0 for p in periods},
    customers[0]: {1: 20, 2: 90, 3: 50, 4: 30},
    customers[1]: {1: 70,  2: 35,  3: 80,  4: 20},
    customers[2]: {1: 60,  2: 80,  3: 60,  4: 15},
    customers[3]: {1: 40,  2: 100, 3: 70,  4: 15}
}

revenue = {
    customers[0]: 40,
    customers[1]: 35,
    customers[2]: 70,
    customers[3]: 80
}

alpha = {
    carriers[0]: 2
}

node_coordinates = {
    depots[0]:      (48.381349031151075, 10.875335320909437),   #Betapharm (von den Koordinaten her Oberhausen Bhf. Apotheke)
    customers[0]:   (48.372725678347464, 10.851883823725666),   #Luther King Apotheke
    customers[1]:   (48.37717621931016, 10.838580109918029),    #Apotheke Via Claudia
    customers[2]:   (48.36988505176495, 10.904548318918328),    #Pelikan Apotheke
    customers[3]:   (48.36887051624558, 10.893702098585257),    #Grottenau Apotheke
    #customers[13]:  (5, 8)
}



#------------------------------------------------------------------------#
#----------------------------Assigning Values----------------------------#
#------------------------------------------------------------------------#

#Maximum capacity if all the carriers
Q_max = max(Q_max_k.values())

#Maximum Duration for each Vehicle
T_max = 170

#Maximum time units difference
delta = 7




#------------------------------------------------------------------------#
#---------------------Calculate Matplotlib Values------------------------#
#------------------------------------------------------------------------#

duration_plt = {(i,j): np.hypot(node_coordinates[i][0] - node_coordinates[j][0], node_coordinates[i][1] - node_coordinates[j][1]) * 100
                   for i in nodes for j in nodes}
cost_plt = {(i,j): duration_plt[i,j] * 0.8
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

#Functions to load and save
def load_file(file):
    with open(file, 'rb') as fp:
        data = pickle.load(fp)
    return data

def save_file(name, file):
    with open(name, 'wb') as fp: 
        pickle.dump(file, fp, protocol=pickle.HIGHEST_PROTOCOL)

#--------------------Normal Execution----------------------------#
#Reading values to improve performance
duration_coordinates = load_file('data/carrier_data/carrier_1_duration_c.p')
distance_coordinates = load_file('data/carrier_data/carrier_1_distance_c.p')
cost_coordinates = load_file('data/carrier_data/carrier_1_cost_c.p')


'''
#-------------------First Time Execution-------------------------#
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
save_file('carrier_1_duration_c.p', file=duration_coordinates)
save_file('carrier_1_distance_c.p', file=distance_coordinates)
save_file('carrier_1_cost_c.p', file=cost_coordinates)
'''