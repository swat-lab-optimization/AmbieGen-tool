
import config as cf
import logging as log

def get_test_suite(res, algo):
    """
    It takes the last generation of the population and returns a dictionary of 30 test cases

    Args:
      res: the result of the genetic algorithm

    Returns:
      A dictionary of 30 test cases.
    """
    test_suite = {}
    gen = len(res.history) - 1
    
    population = res.history[gen].pop.get("X")
    if algo != "nsga2":
        population = sorted(population, key=lambda x: abs(x[0].fitness), reverse=True)
    for i in range(cf.ga["test_suite_size"]):
        #result = res.history[gen].pop.get("X")[i][0]
        result = population[i][0]
        states = result.states
        new_states = []
        for state in states:
            new_states.append([int(x) for x in state])
        test_suite[str(i)] = new_states

    log.info("Test suite of %d test scenarios generated", cf.ga["test_suite_size"])
    return test_suite
