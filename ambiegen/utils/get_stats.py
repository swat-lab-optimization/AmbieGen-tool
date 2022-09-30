from itertools import combinations
from ambiegen.utils.calc_novelty import calc_novelty
import numpy as np


def get_stats(res, problem):
    """
    It takes the results of the optimization and returns a dictionary with the fitness, novelty, and
    convergence of the optimization

    Args:
      res: the result of the optimization
      problem: the problem we're trying to solve

    Returns:
      A dictionary with the fitness, novelty, and convergence of the results.
    """

    res_dict = {}
    gen = len(res.history) - 1
    results = []
    for i in range(30):
        result = res.history[gen].pop.get("F")[i][0]
        results.append(abs(result))

    gen = len(res.history) - 1
    novelty_list = []
    for i in combinations(range(0, 30), 2):
        current1 = res.history[gen].pop.get("X")[i[0]]
        current2 = res.history[gen].pop.get("X")[i[1]]
        nov = calc_novelty(current1[0].states, current2[0].states, problem)
        novelty_list.append(nov)
    novelty = sum(novelty_list) / len(novelty_list)

    generations = np.arange(1, len(res.history), 1)
    convergence = [-res.history[gen].pop.get("F")[0][0] for gen in generations]

    res_dict["fitness"] = results
    res_dict["novelty"] = novelty
    res_dict["convergence"] = convergence

    return res_dict
