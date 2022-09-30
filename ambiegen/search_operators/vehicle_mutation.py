import numpy as np
from pymoo.core.mutation import Mutation
import copy
import config as cf


class VehicleMutation(Mutation):
    """
    Module to perform the mutation
    """

    def __init__(self, mut_rate):
        super().__init__()
        self.mut_rate = mut_rate

    def _do(self, problem, X, **kwargs):
        for i in range(len(X)):
            r = np.random.random()
            s = X[i, 0]
            # with a given probability - perform the mutation
            if r < self.mut_rate:

                sn = copy.deepcopy(s)

                wr = np.random.random()
                child = sn.states

                old_states = child

                # exchnage mutation operator, exchange two random states
                if wr < 0.5:

                    candidates = list(np.random.randint(0, high=len(child), size=2))
                    temp = child[candidates[0]]
                    child[candidates[0]] = child[(candidates[1])]
                    child[(candidates[1])] = temp

                # change of value operator, change the value of one of the attributes of a random state
                else:
                    num = np.random.randint(0, high=len(child))

                    if child[(num)][0] == 0:
                        child[(num)][0] = np.random.choice([1, 2])

                    elif child[(num)][0] == 1:
                        child[(num)][0] = np.random.choice([0, 2])
                    elif child[(num)][0] == 2:
                        child[(num)][0] = np.random.choice([0, 1])

                    if child[(num)][0] == 0:
                        value_list = np.arange(
                            cf.vehicle_env["min_len"], cf.vehicle_env["max_len"], 1
                        )
                        child[num][1] = int(np.random.choice(value_list))
                    else:
                        value_list = np.arange(
                            cf.vehicle_env["min_angle"], cf.vehicle_env["max_angle"], 5
                        )
                        child[num][2] = int(np.random.choice(value_list))

                sn.states = child

                X[i, 0] = sn

        return X
