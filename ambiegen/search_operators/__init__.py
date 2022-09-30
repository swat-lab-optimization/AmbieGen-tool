from ambiegen.search_operators.vehicle_crossover import VehicleCrossover
from ambiegen.search_operators.vehicle_mutation import VehicleMutation
from ambiegen.search_operators.robot_crossover import RobotCrossover
from ambiegen.search_operators.robot_mutation import RobotMutation

OPERATORS = {
    'vehicle_crossover': VehicleCrossover,
    'vehicle_mutation': VehicleMutation,
    'robot_crossover': RobotCrossover,
    'robot_mutation': RobotMutation
}