
import logging as log
import numpy as np
from pymoo.core.sampling import Sampling
import config as cf
from ambiegen.utils.car_road import Map
#from ambiegen.utils.vehicle import Car
from ambiegen.solutions import VehicleSolution
from ambiegen.utils.vehicle_evaluate import evaluate_scenario
from ambiegen.utils.vehicle_evaluate import interpolate_road
from ambiegen.utils.road_validity_check import is_valid_road

def generate_random_road():
    """
    It generates a random road topology
    """
    actions = list(range(0, 3))
    lengths = list(range(cf.vehicle_env["min_len"], cf.vehicle_env["max_len"]))
    angles = list(range(cf.vehicle_env["min_angle"], cf.vehicle_env["max_angle"]))

    map_size = cf.vehicle_env["map_size"]

    #speed = 9
    #steer_ang = 12

    fitness = 0
    valid_road = False

    while not(valid_road):  # ensures that the generated road is valid
        done = False
        test_map = Map(map_size)
        #car = Car(speed, steer_ang, map_size)
        while not done:
            action = np.random.choice(actions)
            if action == 0:
                length = np.random.choice(lengths)
                done = not (test_map.go_straight(length))
            elif action == 1:
                angle = np.random.choice(angles)
                done = not (test_map.turn_right(angle))
            elif action == 2:
                angle = np.random.choice(angles)
                done = not (test_map.turn_left(angle))
        scenario = test_map.scenario[:-1]

        road_points, scenario = test_map.get_points_from_states(scenario)
        #intp_points = interpolate_road(road_points)
        #fitness, _ = evaluate_scenario(intp_points)
        valid_road = is_valid_road(road_points)

    return scenario#, fitness


class VehicleSampling(Sampling):

    """
    Module to generate the initial population

    returns: a tensor of candidate solutions
    """

    def _do(self, problem, n_samples, **kwargs):

        X = np.full((n_samples, 1), None, dtype=object)

        for i in range(n_samples):
            states = generate_random_road()
            s = VehicleSolution()
            s.states = states
            #s.fitness = fitness
            X[i, 0] = s

        log.debug("Initial population of %d solutions generated", n_samples)
        return X
