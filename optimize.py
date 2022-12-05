import argparse
import sys
import logging as log

from pymoo.optimize import minimize
from pymoo.termination import get_termination


import config as cf
from ambiegen import ALRGORITHMS
from ambiegen.duplicate_elimination.duplicate_rem import DuplicateElimination
from ambiegen.problems import PROBLEMS
from ambiegen.samplers import SAMPLERS
from ambiegen.search_operators import OPERATORS
from ambiegen.utils.get_convergence import get_convergence
from ambiegen.utils.get_stats import get_stats
from ambiegen.utils.get_test_suite import get_test_suite
from ambiegen.utils.random_seed import get_random_seed
from ambiegen.utils.save_tc_results import save_tc_results
from ambiegen.utils.save_tcs_images import save_tcs_images

def setup_logging(log_to, debug):
    """
    It sets up the logging system
    """
    #def log_exception(extype, value, trace):
    #    log.exception('Uncaught exception:', exc_info=(extype, value, trace))

    term_handler = log.StreamHandler()
    log_handlers = [term_handler]
    #term_handler.setLevel(log.INFO)
    start_msg = "Started test generation"

    if log_to is not None:
        file_handler = log.FileHandler(log_to, 'w', 'utf-8')
        #file_handler.setLevel(log.DEBUG)
        log_handlers.append(file_handler)
        start_msg += " ".join([", writing logs to file: ", str(log_to)])

    log_level = log.DEBUG if debug else log.INFO

    log.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',  level=log_level, handlers=log_handlers, force=True)

    #sys.excepthook = log_exception

    log.info(start_msg)


def parse_arguments():
    '''
    Function for parsing the arguments
    '''
    parser = argparse.ArgumentParser(
                    prog = 'optimize.py',
                    description = 'A tool for generating test cases for autonomous systems',
                    epilog = "For more information, please visit https://github.com/swat-lab-optimization/AmbieGen-tool ")
    parser.add_argument('--problem', type=str, default="vehicle", help='Problem to solve, possivle values: vehicle, robot')
    parser.add_argument('--algorithm', type=str, default="nsga2", help='Algorithm to use, possivle values: nsga2, ga, random')
    parser.add_argument('--runs', type=int, default=1, help='Number of runs')
    parser.add_argument('--save_results', type=str, default=True, help='Save results, possible values: True, False')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')
    parser.add_argument('--debug', type=str, default=False, help='Run in debug mode, possible values: True, False')
    
    arguments = parser.parse_args()
    return arguments


def main(problem, algo, runs_number, save_results, random_seed, debug):
    """
    Function for running the optimization and saving the results"""

    log_file = "logs.txt"



    setup_logging(log_file, debug)

    log.info("Running the optimization")
    log.info("Problem: %s, Algorithm: %s, Runs number: %s, Saving the results: %s", problem, algo, runs_number, save_results)

    if cf.ga["pop_size"] < cf.ga["test_suite_size"]:
        log.error("Population size should be greater or equal to test suite size")
        sys.exit(1)

    n_offsprings = cf.ga["pop_size"]
    algorithm = ALRGORITHMS[algo](
        n_offsprings=n_offsprings,
        pop_size=cf.ga["pop_size"],
        sampling=SAMPLERS[problem](),
        crossover=OPERATORS[problem + "_crossover"](cf.ga["cross_rate"]),
        mutation=OPERATORS[problem + "_mutation"](cf.ga["mut_rate"]),
        eliminate_duplicates=DuplicateElimination(),
        n_points_per_iteration=n_offsprings
    )

    termination = get_termination("n_gen", cf.ga["n_gen"])
    #termination = get_termination("n_eval", 3000)

    tc_stats = {}
    tcs = {}
    tcs_convergence = {}
    for m in range(runs_number):
        log.info("Executing run %d: ", m)
        if random_seed is not None:
            seed = random_seed
        else:
            seed = get_random_seed()

        
        log.info("Using random seed: %s", seed)

        res = minimize(
            PROBLEMS[problem + "_" + algo](),
            algorithm,
            termination,
            seed=seed,
            verbose=True,
            save_history=True,
            eliminate_duplicates=True
        )

        log.info("Execution time, %f sec", res.exec_time)

        test_suite = get_test_suite(res, algo)
        tc_stats["run" + str(m)] = get_stats(res, problem, algo)
        tcs["run" + str(m)] = test_suite

        tcs_convergence["run" + str(m)] = get_convergence(res, n_offsprings)

        if save_results:
            save_tc_results(tc_stats, tcs, tcs_convergence, algo)
            save_tcs_images(test_suite, problem, m, algo)


################################## MAIN ########################################

if __name__ == "__main__":
    args = parse_arguments()
    main(args.problem, args.algorithm, args.runs, args.save_results, args.seed, args.debug)

