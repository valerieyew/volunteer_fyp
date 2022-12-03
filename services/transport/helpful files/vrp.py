from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
# from datetime import datetime
# import googlemaps
import pprint
import itertools
# import pandas as pd
import urllib
import urllib.parse
import urllib.request
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def select_stops(employees_choices, number_of_stops):
    print('employees choices')
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(employees_choices)
    print()

    # iterate through employees_choices, add corresponding weights to the MRT name
    top_stations = {}
    for col in employees_choices:
        # print(f"score = {col[1]}")
        # print(f"station = {col[2]}")
        if col[2] in top_stations:
            top_stations[col[2]] += col[1]
        else:
            top_stations[col[2]] = col[1]
    # sort by value in descending order
    top_stations = dict(sorted(top_stations.items(),
                        key=lambda x: x[1], reverse=True))
    # select top n stations
    top_stations = dict(itertools.islice(
        top_stations.items(), number_of_stops))
    # extract station names
    top_stations = list(top_stations.keys())

    # add volunteering location
    # volunteering_location = 'Changi Business Park Central 1, Credit Suisse AG, Singapore'
    volunteering_location = 'Dhoby Ghaut - MRT, Singapore'
    top_stations.append(volunteering_location)
    stops = top_stations
    # print('stops = ')
    # pp.pprint(stops)
    # print()
    return stops


def send_request(origin_addresses, dest_addresses, API_key):
    """ Build and send request for the given origin and destination addresses."""
    def build_address_str(addresses):
        # Build a pipe-separated string of addresses
        address_str = ''
        for i in range(len(addresses) - 1):
            address_str += addresses[i] + '|'
        address_str += addresses[-1]
        return address_str

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric'
    origin_address_str = urllib.parse.quote(build_address_str(origin_addresses))
    dest_address_str = urllib.parse.quote(build_address_str(dest_addresses))
    request = request + '&origins=' + origin_address_str + '&destinations=' + \
        dest_address_str + '&key=' + API_key
    jsonResult = urllib.request.urlopen(request).read()
    response = json.loads(jsonResult)
    # pprint.pprint(response)
    return response


def build_duration_matrix(response):
    duration_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['duration']['value'] // 60
                    for j in range(len(row['elements']))]
        duration_matrix.append(row_list)
    return duration_matrix

# input: stops
def create_duration_matrix(stops):
    addresses = stops
    print('stops')
    print('# index : MRT names')
    for i in range(len(addresses)):
        print(f"{i} : {addresses[i]}")

    API_key = 'AIzaSyBWcbR4iX_PUyxg3V7IVaBFD-nJvG6Xj1o'
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses)  # 16 in this example.
    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    duration_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        duration_matrix += build_duration_matrix(response)

    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        duration_matrix += build_duration_matrix(response)
    
    print()
    print('duration matrix')
    # print(pd.DataFrame(duration_matrix))
    return duration_matrix


"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Duration are in seconds.
"""


def create_data_model(duration_matrix):
    """Stores the data for the problem."""
    data = {}
    data['duration_matrix'] = duration_matrix
    data['num_vehicles'] = 2
    print()
    print(f"no of shuttle buses = {data['num_vehicles']}")
    print()

    # based on num_vehicles, compute starting points, which are indexes of the furthest point from the volunteering in a list
    last_row = duration_matrix[len(duration_matrix) - 1]
    starting_point_index = sorted(
        range(len(last_row)), key=lambda sub: last_row[sub])[-data['num_vehicles']:]
    # print(f'indexes of the starting point per cluster = {starting_point_index}')
    # print()

    # fix starting and ending points
    data['starts'] = starting_point_index
    # data['starts'] = [4, 7]
    data['ends'] = [len(duration_matrix) - 1] * data['num_vehicles']

    return data


def print_solution(data, manager, routing, solution, stops):
    """Prints solution on console."""
    # print(f'Objective: {solution.ObjectiveValue()}')
    max_route_duration = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_duration = 0
        while not routing.IsEnd(index):
            # print(f'manager.IndexToNode(index) = {manager.IndexToNode(index)}')
            # print(stops[manager.IndexToNode(index)])
            plan_output += '{} -> '.format(stops[manager.IndexToNode(index)])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_duration += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(stops[manager.IndexToNode(index)])
        plan_output += 'Duration of this route: {}min\n'.format(route_duration)
        print(plan_output)
        max_route_duration = max(route_duration, max_route_duration)
    print('Maximum route duration: {}min'.format(max_route_duration))


def main():
    # denotes employee_id, weight and mrt_station_name
    employees_choices = [
        # [1, 3, 'one-north MRT Station (CC23)'],
        # [1, 2, 'Buona Vista MRT Station (CC22)'],
        # [1, 1, 'Kent Ridge MRT Station (CC24)'],
        # [2, 3, 'Holland Village MRT Station (CC21)'],
        # [2, 2, 'Farrer Road MRT Station (CC20)'],
        # [2, 1, 'Buona Vista MRT Station (CC22)'],
        # [3, 3, 'Queenstown MRT Station (EW19)'],
        # [3, 2, 'Redhill MRT Station (EW18)'],
        # [3, 1, 'Commonwealth MRT Station (EW20)'],
        # [4, 3, 'Kent Ridge MRT Station (CC24)'],
        # [4, 2, 'one-north MRT Station (CC23)'],
        # [4, 1, 'Buona Vista MRT Station (CC22)'],
        # [5, 3, 'Kent Ridge MRT Station (CC24)'],
        # [5, 2, 'one-north MRT Station (CC23)'],
        # [5, 1, 'Buona Vista MRT Station (CC22)'],
        # [6, 3, 'Haw Par Villa MRT Station (CC25)'],
        # [6, 2, 'Pasir Panjang MRT Station (CC26)'],
        # [6, 1, 'Labrador Park MRT Station (CC27)'],
        # [7, 3, 'Pasir Panjang MRT Station (CC26)'],
        # [7, 2, 'Labrador Park MRT Station (CC27)'],
        # [7, 1, 'Telok Blangah MRT Station (CC28)'],
        # [8, 3, 'HarbourFront MRT Station (CC29)'],
        # [8, 2, 'Outram Park MRT Station (EW16)'],
        # [8, 1, 'Telok Blangah MRT Station (CC28)'],
        # [9, 3, 'HarbourFront MRT Station (CC29)'],
        # [9, 2, 'Outram Park MRT Station (EW16)'],
        # [9, 1, 'Telok Blangah MRT Station (CC28)'],
        # [10, 3, 'Telok Blangah MRT Station (CC28)'],
        # [10, 2, 'HarbourFront MRT Station (CC29)'],
        # [10, 1, 'Labrador Park MRT Station (CC27)'],
        # [11, 3, 'Tiong Bahru MRT Station (EW17)'],
        # [11, 2, 'Redhill MRT Station (EW18)'],
        # [11, 1, 'Queenstown MRT Station (EW19)'],
        # [12, 3, 'Queenstown MRT Station (EW19)'],
        # [12, 2, 'Redhill MRT Station (EW18)'],
        # [12, 1, 'Tiong Bahru MRT Station (EW17)'],
        # [13, 3, 'Redhill MRT Station (EW18)'],
        # [13, 2, 'Tiong Bahru MRT Station (EW17)'],
        # [13, 1, 'Outram Park MRT Station (EW16)'],
        # [14, 3, 'Outram Park MRT Station (EW16)'],
        # [14, 2, 'Telok Blangah MRT Station (CC28)'],
        # [14, 1, 'Tiong Bahru MRT Station (EW17)'],
        # [15, 3, 'Tiong Bahru MRT Station (EW17)'],
        # [15, 2, 'Redhill MRT Station (EW18)'],
        # [15, 1, 'Queenstown MRT Station (EW19)'],
        # [16, 3, 'Holland Village MRT Station (CC21)'],
        # [16, 2, 'Farrer Road MRT Station (CC20)'],
        # [16, 1, 'Buona Vista MRT Station (CC22)'],
        # [17, 3, 'Holland Village MRT Station (CC21)'],
        # [17, 2, 'Farrer Road MRT Station (CC20)'],
        # [17, 1, 'Buona Vista MRT Station (CC22)'],
        # [18, 3, 'Outram Park MRT Station (EW16)'],
        # [18, 2, 'HarbourFront MRT Station (CC29)'],
        # [18, 1, 'Telok Blangah MRT Station (CC28)'],
        # [19, 3, 'Commonwealth MRT Station (EW20)'],
        # [19, 2, 'Queenstown MRT Station (EW19)'],
        # [19, 1, 'Kent Ridge MRT Station (CC24)'],
        # [20, 3, 'Queenstown MRT Station (EW19)'],
        # [20, 2, 'Haw Par Villa MRT Station (CC25)'],
        # [20, 1, 'Kent Ridge MRT Station (CC24)'],
        [1, 3, 'Jurong East MRT Station (NS1/EW24)'],
        [12, 3, 'Simei MRT Station (EW3)'],
        [3, 3, 'Clementi MRT Station (EW23)'],
        [11, 3, 'Kembangan MRT Station (EW6)'],
        [4, 3, 'Pioneer MRT Station (EW28)'],
        [10, 3, 'Eunos MRT Station (EW7)'],
        [5, 3, 'Commonwealth MRT Station (EW20)'],
        [8, 3, 'Lavender MRT Station (EW11)'],
        [6, 3, 'Buona Vista MRT Station (CC22)'],
        [7, 3, 'Paya Lebar MRT Station (EW7)'],
        [2, 3, 'Bukit Panjang MRT Station (DT1)'],
        [9, 3, 'Kallang MRT Station (EW10)'],
    ]

    number_of_stops = 12
    # stops = select_stops(employees_choices, number_of_stops)
    # duration_matrix = create_duration_matrix(stops)
    data = {}
    stops = select_stops(employees_choices, number_of_stops)
    duration_matrix = create_duration_matrix(stops)
    data = create_data_model(duration_matrix)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['duration_matrix']),
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def duration_callback(from_index, to_index):
        """Returns the duration between the two nodes."""
        # Convert from routing variable Index to duration matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['duration_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(duration_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Duration constraint.
    dimension_name = 'Time'
    routing.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        120,  # maximum time per vehicle: 2 hours
        True,  # start cumul to zero
        dimension_name)
    duration_dimension = routing.GetDimensionOrDie(dimension_name)
    duration_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution, stops)
    else:
        print('No solution found !')


if __name__ == "__main__":
    main()
