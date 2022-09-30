import numpy as np
from pymoo.core.sampling import Sampling
from ambiegen.solutions.robot_solution import RobotSolution
from ambiegen.utils.robot_map import Map
from ambiegen.utils.a_star import AStarPlanner
import config as cf


def generate_random_solution(grid_size, robot_radius, sx, sy, gx, gy):
    """
    Given a grid size, robot radius, start and goal coordinates, generate a random solution

    :param grid_size: the size of the grid (grid_size x grid_size)
    :param robot_radius: radius of the robot
    :param sx: start x position
    :param sy: start y position
    :param gx: goal x coordinate
    :param gy: goal y position
    """

    map_size = cf.robot_env["map_size"]
    path_size = 0
    while path_size < 2:  # if the path is too short, generate a new solution
        states = []
        for i in range(0, map_size - 1):

            ob_type = np.random.randint(0, 2)
            value = np.random.randint(
                cf.robot_env["min_len"], cf.robot_env["max_len"] + 1)
            position = np.random.randint(
                cf.robot_env["min_pos"], cf.robot_env["max_pos"] + 1)
            states.append([ob_type, value, position])
        map_builder = Map(map_size)
        map_points = map_builder.get_points_from_states(states)
        points_list = map_builder.get_points_cords(map_points)
        ox = [t[0] for t in points_list]
        oy = [t[1] for t in points_list]
        a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
        rx, ry, _ = a_star.planning(sx, sy, gx, gy)
        path_size = len(rx)

    return states


class RobotSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        """
        This is a function to generate the initial population of the algorithm

        returns: a tensor of candidate solutions
        """

        X = np.full((n_samples, 1), None, dtype=np.object)

        for i in range(n_samples):
            s = RobotSolution()
            states = generate_random_solution(
                s.grid_size, s.robot_radius, s.sx, s.sy, s.gx, s.gy)
            s.states = states
            X[i, 0] = s

        return X
