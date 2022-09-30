import numpy as np
from pymoo.core.crossover import Crossover
from ambiegen.solutions import VehicleSolution
import random as rm

# this is the crossover operator for the vehicle problem
class VehicleCrossover(Crossover):
    """
    Module to perform the crossover
    """

    def __init__(self, cross_rate):
        super().__init__(2, 2)
        self.cross_rate = cross_rate

    def _do(self, problem, X, **kwargs):
        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, n_var = X.shape

        # The output owith the shape (n_offsprings, n_matings, n_var)
        Y = np.full_like(X, None, dtype=np.object)
        # for each mating provided

        for k in range(n_matings):

            r = np.random.random()

            s_a, s_b = X[0, k, 0], X[1, k, 0]

            if r < self.cross_rate:
                tc_a = s_a.states
                tc_b = s_b.states

                # get the crossover point
                if len(tc_a) < len(tc_b):
                    crossover_point = rm.randint(1, len(tc_a) - 1)
                elif len(tc_b) < len(tc_a):
                    crossover_point = rm.randint(1, len(tc_b) - 1)
                else:
                    crossover_point = rm.randint(1, len(tc_a) - 1)

                if len(s_a.states) > 2 and len(s_b.states) > 2:

                    offa = VehicleSolution()
                    offb = VehicleSolution()

                    # one point crossover

                    offa.states[:crossover_point] = tc_a[:crossover_point]
                    offa.states[crossover_point:] = tc_b[crossover_point:]
                    offb.states[:crossover_point] = tc_b[:crossover_point]
                    offb.states[crossover_point:] = tc_a[crossover_point:]
                    
                    Y[0, k, 0], Y[1, k, 0] = offa, offb

                else:
                    print("Not enough states!")
                    Y[0, k, 0], Y[1, k, 0] = s_a, s_b

                

            else:
                Y[0, k, 0], Y[1, k, 0] = s_a, s_b

        return Y
