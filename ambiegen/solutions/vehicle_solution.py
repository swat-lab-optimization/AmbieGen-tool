

import matplotlib.pyplot as plt

import config as cf
from ambiegen.utils.car_road import Map
from ambiegen.utils.vehicle import Car


class VehicleSolution:

    """
    This is a class to represent one individual of the genetic algorithm
    It also contains the methods to evaluate the fitness of the solution, novelty and build the image
    """

    def __init__(self):

        self.road_points = []
        self.states = []
        self.speed = 9
        self.steer_ang = 12
        self.map_size = cf.vehicle_env["map_size"]
        self.fitness = 0
        self.car_path = []
        self.novelty = 0
        self.intp_points = []
        self.just_fitness = 0

    def eval_fitness(self):
        """
        The function takes a list of states (self.states) and converts them to a list of points
        (self.road_points).
        The function then takes the list of points and interpolates them to create a list of interpolated
        points (self.intp_points).
        The function then takes the list of interpolated points and executes them with the simplified system model
        The function then calculates the fitness of the individual.
        Returns:
          The fitness of the individual.
        """
        test_map = Map(self.map_size)
        car = Car(self.speed, self.steer_ang, self.map_size)
        road_points = test_map.get_points_from_states(self.states)
        self.states = self.states[:len(road_points)-1].copy()
        if len(road_points) <= 2:
            self.fitness = 0
        else:
            intp_points = car.interpolate_road(road_points)
            self.fitness, self.car_path = car.execute_road(
                intp_points
            )

        self.road_points = road_points

        return self.fitness

    # @staticmethod
    def compare_states(self, state1, state2):
        """
        If the two states are the same, then the similarity is 1. If the two states are different, then the
        similarity is 0

        Args:
          state1: the first element to compare
          state2: the secoind element to compare

        Returns:
          The similarity of the two states.
        """
        similarity = 0
        if state1[0] == state2[0]:
            similarity += 1
            if state1[0] == 0:
                if abs(state1[1] - state2[1]) <= 2:
                    similarity += 1
            else:
                if abs(state1[2] - state2[2]) <= 5:
                    similarity += 1

        return similarity

    def calculate_novelty(self, tc1, tc2):
        """
        novelty = calc_novelty(state1, state2, "vehicle")
        return -novelty
        """

        similarity = 0
        state_num = min(len(tc1), len(tc2))

        total_states = state_num * cf.vehicle_env["elem_types"]
        for i in range(state_num):
            similarity += self.compare_states(tc1[i], tc2[i])
        novelty = 1 - (similarity / total_states)

        return -novelty

    @staticmethod
    def build_image(states, save_path="test.png"):
        """
        It takes a list of states, and plots the road and the car path

        Args:
          states: a list of tuples, each tuple is a state of the car.
          save_path: The path to save the image to. Defaults to test.png
        """
        map_size = cf.vehicle_env["map_size"]
        test_map = Map(map_size)
        road_points = test_map.get_points_from_states(states)
        speed = 9
        steer_ang = 12
        car = Car(speed, steer_ang, map_size)
        intp_points = car.interpolate_road(road_points)

        fig, ax = plt.subplots(figsize=(12, 12))
        road_x = []
        road_y = []

        for p in intp_points:
            road_x.append(p[0])
            road_y.append(p[1])

        fitness, car_path = car.execute_road(intp_points)

  
        if len(car_path) > 0:
            ax.plot(car_path[0], car_path[1], "bo", label="Car path")

        ax.plot(road_x, road_y, "yo--", label="Road")

        top = map_size
        bottom = 0

        ax.set_title("Test case fitenss " + str(fitness), fontsize=17)

        ax.set_ylim(bottom, top)
        plt.ioff()
        ax.set_xlim(bottom, top)
        ax.legend()
        fig.savefig(save_path)
        plt.close(fig)