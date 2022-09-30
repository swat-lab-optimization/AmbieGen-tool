from pymoo.core.duplicate import ElementwiseDuplicateElimination

# It's a duplicate elimination that compares the states of the two elements


class DuplicateElimination(ElementwiseDuplicateElimination):

    def is_equal(self, a, b):

        return a.X[0].states == b.X[0].states

