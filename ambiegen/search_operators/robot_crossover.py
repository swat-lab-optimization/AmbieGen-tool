
import random as rm
import numpy as np
from pymoo.core.crossover import Crossover

from ambiegen.solutions import RobotSolution


# this is the crossover operator for the robot problem
class RobotCrossover(Crossover):
    """
    Class to define the crossover operator for the robot problem
    """
    def __init__(self, cross_rate):

        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)
        self.cross_rate = cross_rate

    def _do(self, problem, X, **kwargs):
        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, _ = X.shape
        # The output owith the shape (n_offsprings, n_matings, n_var)

        Y = np.full_like(X, None, dtype=np.object)

        # for each mating provided
        for k in range(n_matings):
            r = np.random.random()

            s_a, s_b = X[0, k, 0], X[1, k, 0]

            if r < self.cross_rate:

                tc_a = s_a.states.copy()
                tc_b = s_b.states.copy()

                # select a random point to crossover
                crossover_point = rm.randint(5, len(tc_b) - 5)

                off_a = RobotSolution()
                off_b = RobotSolution()

                # perform a one point crossover

                off_a.states[:crossover_point] = tc_a[:crossover_point]
                off_a.states[crossover_point:] = tc_b[crossover_point:]
                off_b.states[:crossover_point] = tc_b[:crossover_point]
                off_b.states[crossover_point:] = tc_a[crossover_point:]

                Y[0, k, 0], Y[1, k, 0] = off_a, off_b

            else:
                Y[0, k, 0], Y[1, k, 0] = s_a, s_b

        return Y
