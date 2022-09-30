import numpy as np


def get_test_suite(res):
    """
    It takes the last generation of the population and returns a dictionary of 30 test cases

    Args:
      res: the result of the genetic algorithm

    Returns:
      A dictionary of 30 test cases.
    """
    test_suite = {}
    gen = len(res.history) - 1

    for i in range(30):
        result = res.history[gen].pop.get("X")[i][0]
        states = result.states
        new_states = []
        for state in states:
            new_states.append([int(x) for x in state])
        test_suite[str(i)] = new_states

    return test_suite
