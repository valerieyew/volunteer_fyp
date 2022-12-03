from coordinates import get_coords_of_single_location

# for pre-optimization
def get_data_consolidated(data, final_venue):
    data_numbers = {}
    # {'Tuas Crescent MRT Station': 6,
    #  'Pioneer MRT Station': 18,}

    data_coordinates = {}
    # {'Tuas Crescent MRT Station': ['1.32102695188066', '103.649078232635'],
    #  'Pioneer MRT Station': ['1.33758688240768', '103.697321513018']}

    data_list = []
    # unique locations
    # [['Tuas Crescent MRT Station', '1.32102695188066', '103.649078232635'],
    #  ['Pioneer MRT Station', '1.33758688240768', '103.697321513018']]

    for location in data:
        if data_numbers.get(location[0]) is not None:
            no_of_this_location = data_numbers[location[0]]
            no_of_this_location += 1
            data_numbers[location[0]] = no_of_this_location
        else:
            data_numbers[location[0]] = 1
            data_coordinates[location[0]] = location[1:3]
            data_list.append(location)
            
    data_list_with_final_venue = data_list.copy()
    data_list_with_final_venue.append(final_venue)
            
    return data_numbers, data_coordinates, data_list, data_list_with_final_venue


# for pre-optimization
def add_coordinates_to_locations(coordinates, data, final_venue):
    # add coordinates to locations list
    for location in data:
        coords = get_coords_of_single_location(coordinates, location[0].rpartition(' MRT')[0])
        for coord in coords:
            location.append(coord)

    # add coordinates to final venue
    final_venue_coords = get_coords_of_single_location(coordinates, final_venue[0].rpartition(' MRT')[0])
    for coord in final_venue_coords:
        final_venue.append(coord)