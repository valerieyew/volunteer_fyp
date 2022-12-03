import urllib.request
import numpy as np
import json

# OSRM is only called once at the start to build the overall time matrix list
# Later time matrices needed is obtained from this overall time matrix list

# for pre-optimization
# concatenate all the coordinates of the MRT stations
# returns request url for osrm
def build_request_for_osrm(data_coordinates, final_venue):
    new_addresses = data_coordinates.copy()
    
    # add final venue to the dictionary if not inside
    if new_addresses.get(final_venue[0]) is None:
        new_addresses[final_venue[0]] = final_venue[1:3]
    
    coordinates_string = ""
    for key in new_addresses.keys():
        coordinates_string += str(new_addresses[key][1]) # add longitude
        coordinates_string += ","
        coordinates_string += str(new_addresses[key][0]) # add latitude
        coordinates_string += ";"
    coordinates_string = coordinates_string[:-1]
    
    # new_request = 'http://localhost:5000/table/v1/driving/' + coordinates_string + "?annotations=duration"
    new_request = 'http://ec2-54-169-10-10.ap-southeast-1.compute.amazonaws.com:5000/table/v1/driving/' + coordinates_string + "?annotations=duration"
    
    return new_request


# form request url and call osrm with it
def get_time_matrix_from_osrm(data_coordinates, final_venue):
    # concatenate their coordinates and send to osrm to get their time matrix
    new_request = build_request_for_osrm(data_coordinates, final_venue)
    # print(new_request)
    
    jsonResult = urllib.request.urlopen(new_request).read()
    response = json.loads(jsonResult)
    
    return np.array(response['durations']) # distances[i][j] is from i-th source to j-th destination


# translate the 2D time matrix array into a list of dictionaries
# [{'source': ['Tuas Crescent MRT Station (EW31)', '1.32102695188066', '103.649078232635'],
#   'destination': ['Woodlands MRT Station (NS9)', '1.43606698186149', '103.787930806962'],
#   'duration': 1517.1}]
def build_overall_time_matrix_list(data_list_with_final_venue, overall_time_matrix):
    time_matrix_list = []
    for i in range(len(data_list_with_final_venue)): 
        for j in range(len(data_list_with_final_venue)):
            location_pair_dict = {}
            location_pair_dict["source"] = data_list_with_final_venue[i]
            location_pair_dict["destination"] = data_list_with_final_venue[j]
            location_pair_dict["duration"] = overall_time_matrix[i][j]
            
            time_matrix_list.append(location_pair_dict)
    
    return time_matrix_list


# Form another time matrix dictionary for faster search:
# {'Tuas Crescent MRT Station (EW31)': {
#     'Tuas Crescent MRT Station (EW31)': 0.0
#     'Woodlands MRT Station (NS9)': 1517.1
#    }
# }
def get_faster_overall_matrix(overall_time_matrix_list, data_list_with_final_venue):
    location_list_without_coordinates = [item[0] for item in data_list_with_final_venue]
    faster_overall_time_matrix_list = {item: {} for item in location_list_without_coordinates}
    current_key = overall_time_matrix_list[0]["source"][0]

    for location_pair in overall_time_matrix_list:
        if location_pair["source"][0] == current_key:
            faster_overall_time_matrix_list[current_key][location_pair["destination"][0]] = location_pair["duration"]
        else:
            current_key = location_pair["source"][0]
            faster_overall_time_matrix_list[current_key][location_pair["destination"][0]] = location_pair["duration"]
    
    return faster_overall_time_matrix_list


# location_list: all the locations to generate this time matrix for
def form_matrix_from_overall_list(location_list, faster_overall_time_matrix_list):
    matrix_size = len(location_list)
    matrix_array = np.zeros((matrix_size, matrix_size))
    
    for i in range(len(location_list)):
        for j in range(len(location_list)): 
            source_location_key = location_list[i][0]
            destination_location_key = location_list[j][0]
            matrix_array[i][j] = faster_overall_time_matrix_list[source_location_key][destination_location_key]

    # print("Matrix array:", matrix_array)
    return matrix_array