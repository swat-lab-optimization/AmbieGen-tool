
import json

import numpy as np

from scipy.interpolate import splprep, splev
from shapely.geometry import LineString, Point
from numpy.ma import arange
import math
import matplotlib.pyplot as plt 
from shapely.geometry import LineString, Polygon
from descartes import PolygonPatch
from ambiegen.utils.car_road import Map

from ambiegen.utils.lane_controller import LaneController
from ambiegen.utils.kinematic_model import KinematicModel
from ambiegen.utils.road_validity_check import is_valid_road

#from simulator.code_pipeline.tests_generation import RoadTestFactory
#from simulator.code_pipeline.validation import TestValidator

def interpolate_road(road):
        """
        It takes a list of points (road) and returns a list of points (nodes) that are evenly spaced
        along the road

        Args:
          road: a list of tuples, each tuple is a point on the road

        Returns:
          A list of tuples.
        """

        test_road = LineString([(t[0], t[1]) for t in road])

        length = test_road.length

        num_nodes = int(length)
        if num_nodes < 20:
            num_nodes = 20

        old_x_vals = [t[0] for t in road]
        old_y_vals = [t[1] for t in road]

        if len(old_x_vals) == 2:
            k = 1
        elif len(old_x_vals) == 3:
            k = 2
        else:
            k = 3
        f2, u = splprep([old_x_vals, old_y_vals], s=0, k=k)

        step_size = 1 / num_nodes *5

        xnew = arange(0, 1 + step_size, step_size)

        x2, y2 = splev(xnew, f2)

        nodes = list(zip(x2, y2))

        return nodes


def build_tc(road_points, car_path, fitness, path):
    """
    This function builds a reperesentation of a test case with a road and a car path, and saves it as an image file.
    
    Args:
      road_points: a list of tuples representing the points on the road
      car_path: The path taken by the car, represented as a tuple of two lists - the x-coordinates and
    y-coordinates of the points on the path.
      fitness: The fitness value of a test case. It is used to display the fitness value in the title of
    the plot.
      path: The path parameter is a string representing the file path where the generated plot will be
    saved.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    road_x = []
    road_y = []

    for p in road_points:
        road_x.append(p[0])
        road_y.append(p[1])

    ax.plot(car_path[0], car_path[1], "bo", label="Car path")

    ax.plot(road_x, road_y, "yo--", label="Road")

    top = 200
    bottom = 0

    road_poly = LineString([(t[0], t[1]) for t in road_points]).buffer(8.0, cap_style=2, join_style=2)
    road_patch = PolygonPatch((road_poly), fc='gray', ec='dimgray')  # ec='#555555', alpha=0.5, zorder=4)
    ax.add_patch(road_patch)

    ax.set_title("Test case fitenss " + str(fitness), fontsize=17)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.legend(fontsize=16)
    ax.set_ylim(bottom, top)
    plt.ioff()
    ax.set_xlim(bottom, top)
    ax.legend()
    fig.savefig(path)
    plt.close(fig)

def evaluate_scenario(points):
    """
    The function evaluates a scenario by simulating a vehicle's path along a set of waypoints and
    returns the negative fitness value and the path coordinates.
    
    Args:
      points: a list of tuples representing the waypoints of a road, where each tuple contains the x and
    y coordinates of a waypoint.
    
    Returns:
      The function `evaluate_scenario` returns a tuple containing the fitness value and a list of x and
    y coordinates of the vehicle's path. The fitness value is the negative of the maximum distance
    traveled by the vehicle on a valid road scenario.
    """

    tot_x = []
    tot_y = []
    

    if is_valid_road(points):
    #if is_valid:

        init_pos = points[0]
        x0 = init_pos[0]
        y0 = init_pos[1]
        yaw0 = 0#get_angle(points[1], points[0]) #0
        speed0 = 15  # 12
        waypoints = points
        vehicle = KinematicModel(x0, y0, yaw0, speed0)
        controller = LaneController(waypoints, speed0)
        done = False
        distance_list = [0]
        steering = 0
        count = 0
        dt = 0.7
        while not(done):
            x, y, yaw, speed = vehicle.x, vehicle.y, vehicle.yaw, vehicle.speed
            steering, speed, distance, done = controller.control(x, y, yaw, speed)
            vehicle.update(steering, 0.1, dt, speed)  #accel = 0.05, v0 = 12
            tot_x.append(vehicle.x)
            tot_y.append(vehicle.y)
            count += 1
            if count > 7:
                #if distance < 7.5:
                distance_list.append(distance)

            #build_tc(points, [tot_x, tot_y], max(distance_list))

        car_path = LineString(zip(tot_x, tot_y))
        if car_path.is_simple is False:
            distance_list2 = [min(3, i) for i in distance_list]
        else:
            distance_list2 = distance_list


        if (distance_list[:-1]):
            fitness = max(distance_list2[:-1])
        else:
            fitness = max(distance_list2)

    else: 
        fitness = 0


    return -fitness, [tot_x[:-1], tot_y[:-1]]
   