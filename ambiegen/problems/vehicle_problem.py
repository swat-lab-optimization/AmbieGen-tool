import logging as log
from pymoo.core.problem import ElementwiseProblem


class VehicleProblem1Obj(ElementwiseProblem):
    '''
    Module to calculate the fitness of the individuals
    '''

    def __init__(self):
        super().__init__(n_var=1, n_obj=1, n_ieq_constr=1)

    def _evaluate(self, x, out, *args, **kwargs):
        """
        > This function evaluates the individual's fitness and novelty
        Individual is stored in the input vector x

        :param x: the input individual
        :param out: the fitness of the individual as well as the constraint
        """
        s = x[0]
        s.fitness = s.eval_fitness()
        out["F"] = s.fitness
        out["G"] = 5 - s.fitness * (-1)

        log.debug("Evaluated individual %s, fitness %s", s, s.fitness)


class VehicleProblem2Obj(ElementwiseProblem):
    '''
    Module to calculate the fitnes of the individuals
    '''

    def __init__(self):
        super().__init__(n_var=1, n_obj=2, n_ieq_constr=1)

    def _evaluate(self, x, out, *args, **kwargs):
        """
        > This function evaluates the individual's fitness and novelty
        Individual is stored in the input vector x

        :param x: the input individual
        :param out: the fitness and novelty of the individual as well as the constraint
        """
        s = x[0]
        s.fitness = s.eval_fitness()
        algorithm = kwargs["algorithm"]

        solutions = algorithm.pop.get("X")
        if (solutions.size > 0) and (s.fitness < -1):
            top_solutions = solutions[0:5]
            best_scenarios = [top_solutions[i]
                              [0].states for i in range(len(top_solutions))]

            novelty_list = []
            for i in range(len(best_scenarios)):
                nov = s.calculate_novelty(best_scenarios[i], s.states)
                novelty_list.append(nov)
            s.novelty = sum(novelty_list)/len(novelty_list)
        else:
            s.novelty = 0

        out["F"] = [s.fitness, s.novelty]
        out["G"] =  5 - s.fitness * (-1)

        log.debug("Evaluated individual %s, fitness %s, novelty %s", s, s.fitness, s.novelty)
