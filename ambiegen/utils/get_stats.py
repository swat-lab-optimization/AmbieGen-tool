from itertools import combinations
from ambiegen.utils.calc_novelty import calc_novelty
import config as cf

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
    population = -res.history[gen].pop.get("F")
    population = sorted(population, key=lambda x: x[0], reverse=True)
    for i in range(cf.ga["test_suite_size"]):


        #result = res.history[gen].pop.get("F")[i][0]
        results.append(population[i][0])

    gen = len(res.history) - 1
    novelty_list = []
    for i in combinations(range(0, cf.ga["test_suite_size"]), 2):
        current1 = res.history[gen].pop.get("X")[i[0]]
        current2 = res.history[gen].pop.get("X")[i[1]]
        nov = calc_novelty(current1[0].states, current2[0].states, problem)
        novelty_list.append(nov)
    novelty = sum(novelty_list) / len(novelty_list)

    res_dict["fitness"] = results
    res_dict["novelty"] = novelty

    return res_dict