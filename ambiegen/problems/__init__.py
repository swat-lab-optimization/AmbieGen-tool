from ambiegen.problems.robot_problem import RobotProblem1Obj, RobotProblem2Obj
from ambiegen.problems.vehicle_problem import VehicleProblem1Obj, VehicleProblem2Obj


PROBLEMS = {
    "vehicle_ga": VehicleProblem1Obj,
    "vehicle_nsga2": VehicleProblem2Obj,
    "robot_ga": RobotProblem1Obj,
    "robot_nsga2": RobotProblem2Obj,
    "robot_random": RobotProblem1Obj,
    "vehicle_random": VehicleProblem1Obj,
}
