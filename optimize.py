from pymoo.termination import get_termination

import config as cf
from pymoo.optimize import minimize
from ambiegen import ALRGORITHMS
from ambiegen.problems import PROBLEMS
from ambiegen.samplers import SAMPLERS
from ambiegen.search_operators import OPERATORS
from ambiegen.duplicate_elimination.duplicate_rem import DuplicateElimination
from ambiegen.utils.random_seed import get_random_seed
from ambiegen.utils.get_stats import get_stats
from ambiegen.utils.get_test_suite import get_test_suite
from ambiegen.utils.save_tc_results import save_tc_results
from ambiegen.utils.save_tcs_images import save_tcs_images


def main(problem, algo, runs_number, save_results=True, save_images=True):


    algorithm = ALRGORITHMS[algo](
        n_offsprings=cf.ga["pop_size"],
        pop_size=cf.ga["pop_size"],
        sampling=SAMPLERS[problem](),
        crossover=OPERATORS[problem + "_crossover"](cf.ga["cross_rate"]),
        mutation=OPERATORS[problem + "_mutation"](cf.ga["mut_rate"]),
        eliminate_duplicates=DuplicateElimination(),
    )

    termination = get_termination("n_gen", cf.ga["n_gen"])

    tc_stats = {}
    tcs = {}
    for m in range(runs_number):
        print("Run: ", m)
        seed = get_random_seed()

        res = minimize(
            PROBLEMS[problem + "_" + algo](),
            algorithm,
            termination,
            seed=seed,
            verbose=True,
            save_history=True,
            eliminate_duplicates=True,
        )

        print("Execution time, sec ", res.exec_time)

        test_suite = get_test_suite(res)
        tc_stats["run" + str(m)] = get_stats(res, problem)
        tcs["run" + str(m)] = test_suite

        if save_results:
            save_tc_results(tc_stats, tcs)
        if save_images:
            save_tcs_images(test_suite, problem, m)


################################## MAIN ########################################
problem = "vehicle"
algo = "ga"
runs_number = 1
if __name__ == "__main__":
    main(problem, algo, runs_number)
