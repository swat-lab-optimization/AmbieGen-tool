import copy
from pymoo.core.mutation import Mutation
import logging as log
import numpy as np
import config as cf

# this is the mutation operator for the robot problem
class RobotMutation(Mutation):
    """
    Class to define the mutation operator for the robot problem
    """
    def __init__(self, mut_rate):
        super().__init__()
        self.mut_rate = mut_rate

    def _do(self, problem, X, **kwargs):

        for i in range(len(X)):
            r = np.random.random()
            s = X[i, 0]
            if r < self.mut_rate:
                log.debug("Performing mutation on individual %s", s)
                sn = copy.deepcopy(s)
                wr = np.random.random()
                child = copy.deepcopy(sn.states)
                n = np.random.randint(2, 6)
                # exchnage mutation operator, exchange two random states
                if wr < 0.5:
                    while n > 0:
                        log.debug("Exchange mutation performed on individual %s", s)
                        candidates = list(np.random.randint(0, high=len(child), size=2))
                        temp = child[candidates[0]]
                        child[candidates[0]] = child[candidates[1]]
                        child[candidates[1]] = temp
                        n -= 1
                # change of value operator, change the value of one of the attributes of a random state
                else:
                    while n > 0:
                        log.debug("Change of value mutation performed on individual %s", s)
                        num = np.random.randint(0, high=len(child))
                        value = np.random.choice(["state", "value", "position"])

                        if value == "value":
                            duration_list = [
                                i
                                for i in range(
                                    cf.robot_env["min_len"], cf.robot_env["max_len"] + 1, 1
                                )
                            ]
                            child[num][1] = int(np.random.choice(duration_list))
                        elif value == "state":
                            if child[num][0] == 0:
                                child[num][0] = 1
                            else:
                                child[num][0] = 0
                        elif value == "position":
                            duration_list = [
                                i
                                for i in range(
                                    cf.robot_env["min_len"],
                                    cf.robot_env["map_size"] - cf.robot_env["min_len"],
                                    1,
                                )
                            ]
                            child[num][2] = int(np.random.choice(duration_list))
                        n -= 1

                sn.states = child.copy()
                X[i, 0] = sn

        return X