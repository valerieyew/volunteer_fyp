import json
import os
from typing import final

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import pandas as pd

from service.all_data import buses
from service.data_processing import add_coordinates_to_locations, get_data_consolidated
from service.time_matrix import get_time_matrix_from_osrm, build_overall_time_matrix_list, get_faster_overall_matrix
from service.bus_combis import get_min_and_max_no_of_clusters, get_bus_capacities, get_bus_combis_without_sorting, get_sorted_bus_combis
from service.libs_adjustments import adjust_lists_for_single_cluster, processing_for_clusters_with_long_durations
from service.kmeans import fit_kmeans, get_clustered_locations_list_before_tsp
from service.tsp import get_tsp_permutations_and_durations, build_dict_with_location_name_and_no_of_ppl
from service.cost import get_cost_and_durations_in_mins
from service.overall_result import print_overall_complete_solution_before_optimization, get_overall_dict_for_optimization, \
    format_solution_for_frontend, pretty_print_dict
from service.optimization import optimize_on_all_n_clusters_in_overall_dict, get_lowest_cost_solution


# 29th April 2022: this is not updated, check app2.py for the latest non-dockerized code
# only need the service folder and app2.py to run

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 100,
    'pool_recycle': 280,
}

db = SQLAlchemy(app)
CORS(app)


class Session_Attendee(db.Model):
    __tablename__ = 'sessions_attendees'

    session_id = db.Column(db.Integer, db.ForeignKey(
        'sessions.session_id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(
        'events.event_id'), nullable=False)
    employee_id = db.Column(db.String(30), nullable=False, primary_key=True)
    point = db.Column(db.String(50), nullable=False)

    def __init__(self, session_id, event_id, employee_id, point):
        self.session_id = session_id
        self.event_id = event_id
        self.employee_id = employee_id
        self.point = point

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "event_id": self.event_id,
            "employee_id": self.employee_id,
            "point": self.point
        }


class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    proposal_details = db.Column(db.String(500), nullable=False)
    info = db.Column(db.String(700), nullable=False)
    registration_opens_on = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    registration_closes_on = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(15), nullable=False)
    comments = db.Column(db.String(700), nullable=False)
    last_admin_action_by = db.Column(db.String(30), nullable=False)

    def __init__(self, event_id, employee_id, name, location, proposal_details, info,
                 registration_opens_on, registration_closes_on, status, comments, last_admin_action_by):
        self.event_id = event_id
        self.employee_id = employee_id
        self.name = name
        self.location = location
        self.proposal_details = proposal_details
        self.info = info
        self.registration_opens_on = registration_opens_on
        self.registration_closes_on = registration_closes_on
        self.status = status
        self.comments = comments
        self.last_admin_action_by = last_admin_action_by

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "employee_id": self.employee_id,
            "name": self.name,
            "location": self.location,
            "proposal_details": self.proposal_details,
            "info": self.info,
            "registration_opens_on": self.registration_opens_on,
            "registration_closes_on": self.registration_closes_on,
            "status": self.status,
            "comments": self.comments,
            "last_admin_action_by": self.last_admin_action_by
        }


def get_data(event_id, session_id):
    session_attendees = Session_Attendee.query.filter_by(
        event_id=event_id,
        session_id=session_id
    ).all()

    attendees = []
    for session_attendee in session_attendees:
        location = []
        session_attendee = session_attendee.to_dict()
        location.append(session_attendee['point'])
        attendees.append(location)

    return attendees


@app.route("/health")
def health_check():
    return jsonify(
        message="Welcome to CS480 FYP by Team Vision (transport)!"
    ), 200


@app.route("/optimize/<int:event_id>/<int:session_id>")
def optimization(event_id, session_id):

    data = get_data(event_id, session_id)
    if len(data) == 0:
        return jsonify(
            message="No participants."
        ), 404

    event_dict = Event.query.filter_by(
        event_id=event_id
    ).first().to_dict()

    final_venue = []
    final_venue.append(event_dict['location'])

    coordinates = pd.read_csv("src/service/coords.csv",
                              low_memory=False, lineterminator='\n')

    # add coordinates to the locations incl. final venue
    add_coordinates_to_locations(coordinates, data, final_venue)

    # get the various lists needed
    data_numbers, data_coordinates, data_list, data_list_with_final_venue = get_data_consolidated(
        data, final_venue)

    total_passengers = len(data)

    # Time matrix
    overall_time_matrix = get_time_matrix_from_osrm(
        data_coordinates, final_venue)  # using dictionary of unique locations
    overall_time_matrix_list = build_overall_time_matrix_list(
        data_list_with_final_venue, overall_time_matrix)  # using list of unique locations

    faster_overall_time_matrix_list = get_faster_overall_matrix(
        overall_time_matrix_list, data_list_with_final_venue)

    # Bus combis
    bus_capacities = get_bus_capacities(buses)
    min_cluster, max_cluster = get_min_and_max_no_of_clusters(
        total_passengers, bus_capacities)

    bus_combis_before_sorting_by_cost = get_bus_combis_without_sorting(
        min_cluster, max_cluster, total_passengers, bus_capacities)
    bus_combinations = get_sorted_bus_combis(
        min_cluster, max_cluster, bus_combis_before_sorting_by_cost, buses)

    # Kmeans lib won't be able to take in 1 as no of clusters
    if_single_cluster_exist = False
    if min_cluster == 1:
        if_single_cluster_exist = True
        min_cluster = 2

    # Kmeans clustering
    sorted_no_of_people_in_each_cluster, no_of_people_in_each_cluster, cluster_allocations_of_locations, \
        chosen_bus_combis, chosen_bus_combis_indexes, selected_cluster_sizes = \
        fit_kmeans(data, min_cluster, max_cluster, bus_combinations)

    clustered_locations_list_before_tsp = get_clustered_locations_list_before_tsp(selected_cluster_sizes, cluster_allocations_of_locations, data,
                                                                                  sorted_no_of_people_in_each_cluster, no_of_people_in_each_cluster)

    # Adjust lists for the single clusters
    if if_single_cluster_exist:
        adjust_lists_for_single_cluster(data_list, total_passengers, bus_capacities, clustered_locations_list_before_tsp,
                                        sorted_no_of_people_in_each_cluster, chosen_bus_combis)

    # Clustering and TSP results with costs before optimization
    clustered_locations_list_after_tsp, tsp_durations = get_tsp_permutations_and_durations(
        clustered_locations_list_before_tsp, faster_overall_time_matrix_list, final_venue)
    default_costs, tsp_durations_in_mins = get_cost_and_durations_in_mins(tsp_durations, chosen_bus_combis, buses)

    # Processing before optimization of results
    if if_single_cluster_exist:
        selected_cluster_sizes.insert(0, 1)
    locations_with_no_of_ppl = build_dict_with_location_name_and_no_of_ppl(
        clustered_locations_list_after_tsp, data_numbers, final_venue)
    overall_dict = get_overall_dict_for_optimization(selected_cluster_sizes, default_costs, sorted_no_of_people_in_each_cluster,
                                                     chosen_bus_combis, tsp_durations_in_mins, locations_with_no_of_ppl,
                                                     clustered_locations_list_after_tsp)

    # Optimization
    optimize_on_all_n_clusters_in_overall_dict(
        selected_cluster_sizes, overall_dict, buses, bus_capacities, faster_overall_time_matrix_list, final_venue)

    # Get lowest cost solution
    lowest_cost_solution = get_lowest_cost_solution(
        selected_cluster_sizes, overall_dict)

    # Format solution for frontend
    output = format_solution_for_frontend(lowest_cost_solution, final_venue)

    return jsonify(output), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
