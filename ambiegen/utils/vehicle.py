import math as m
import numpy as np

from scipy.interpolate import splprep, splev
from shapely.geometry import LineString, Point
from numpy.ma import arange

import config as cf


class Car:
    """
    Class to execute the simplified car model
    given a set of the inpput points defining the road topology
    """

    def __init__(self, speed, steer_ang, map_size):
        self.speed = speed
        self.map_size = map_size
        self.str_ang = steer_ang
        self.str_ang_o = steer_ang
        self.x = 0
        self.y = 0
        self.distance = 0
        self.angle = 0
        self.tot_x = []
        self.tot_y = []
        self.tot_dist = []

        

    def interpolate_road(self, road):
        """
        It takes a list of points (road) and returns a list of points (nodes) that are evenly spaced
        along the road

        Args:
          road: a list of tuples, each tuple is a point on the road

        Returns:
          A list of tuples.
        """

        test_road = LineString([(t[0], t[1]) for t in road])

        length = test_road.length

        num_nodes = int(length)
        if num_nodes < 20:
            num_nodes = 20

        old_x_vals = [t[0] for t in road]
        old_y_vals = [t[1] for t in road]

        if len(old_x_vals) == 2:
            k = 1
        elif len(old_x_vals) == 3:
            k = 2
        else:
            k = 3
        f2, u = splprep([old_x_vals, old_y_vals], s=0, k=k)

        step_size = 1 / num_nodes

        xnew = arange(0, 1 + step_size, step_size)

        x2, y2 = splev(xnew, f2)

        nodes = list(zip(x2, y2))

        return nodes

    def get_distance(self, road, x, y):
        """
        > The function takes a road and a point and returns the distance from the point to the road

        Args:
          road: a list of points that make up the road
          x: the x coordinate of the point
          y: the y-coordinate of the point

        Returns:
          The distance between the point and the road.
        """
        p = Point(x, y)
        return p.distance(road)

    def go_straight(self):
        """
        The function takes the current x and y coordinates of the car, the current angle of the car, and the
        speed of the car, and returns the new x and y coordinates of the car after it has moved forward

        Returns:
          nothing.
        """
        self.x = self.speed * np.cos(m.radians(self.angle)) / 2.3 + self.x
        self.y = self.speed * np.sin(m.radians(self.angle)) / 2.3 + self.y
        self.tot_x.append(self.x)
        self.tot_y.append(self.y)
        return

    def turn_right(self):
        """
        The function takes the current x and y coordinates of the car, the current angle of the car, the
        speed of the car. It then calculates the angle the
        car needs to turn to make a right turn, and then calculates the new x and y coordinates of the car

        Returns:
          nothing.
        """

        self.str_ang = m.degrees(m.atan(1 / self.speed * 2 * self.distance))
        self.angle = -self.str_ang + self.angle
        self.x = self.speed * np.cos(m.radians(self.angle)) / 3 + self.x
        self.y = self.speed * np.sin(m.radians(self.angle)) / 3 + self.y
        self.tot_x.append(self.x)
        self.tot_y.append(self.y)
        return

    def turn_left(self):
        """
        The function takes the current x and y coordinates of the car, the current angle of the car, the
        speed of the car,  and returns the new x and y coordinates of
        the car after it has turned left

        Returns:
          nothing.
        """
        self.str_ang = m.degrees(m.atan(1 / self.speed * 2 * self.distance))
        self.angle = self.str_ang + self.angle
        self.x = self.speed * np.cos(m.radians(self.angle)) / 3 + self.x
        self.y = self.speed * np.sin(m.radians(self.angle)) / 3 + self.y

        self.tot_x.append(self.x)
        self.tot_y.append(self.y)

        return

    def get_angle(self, node_a, node_b):
        """
        It takes two points, and returns the angle between them

        Args:
          node_a: The first node
          node_b: the node that is being rotated

        Returns:
          The angle between the two nodes.
        """
        vector = np.array(node_b) - np.array(node_a)
        cos = vector[0] / (np.linalg.norm(vector))

        angle = m.degrees(m.acos(cos))

        if node_a[1] > node_b[1]:
            return -angle
        else:
            return angle

    def execute_road(self, int_points):
        """
        The function takes in a list of points, and then creates a road from those points. It then
        "drives" the car along the road. The car is controlled by a simple algorithm
        that tries to keep the car as close to the road as possible. The fitness of the road is
        determined by how far the car is from the road at the end of the simulation

        Args:
          int_points: the interpolated points of the road

        Returns:
          The fitness and the coodinates of te total x and y values the car travelled
        """

        nodes = [[p[0], p[1]] for p in int_points]

        road = LineString([(t[0], t[1]) for t in nodes])

        valid = (road.is_simple is False) or (is_too_sharp(_interpolate(nodes)))

        if valid is True:
            self.tot_x = []
            self.tot_y = []
            fitness = 0
        else:

            self.x = 0
            self.y = 0

            self.angle = 0
            self.tot_x = []
            self.tot_y = []
            self.tot_dist = []
            self.distance = 0

            mini_nodes1 = nodes[: round(len(nodes) / 2)]
            mini_nodes2 = nodes[round(len(nodes) / 2) :]
            if (len(mini_nodes1) < 2) or (len(mini_nodes2) < 2):
                return 0, []
            mini_road1 = LineString([(t[0], t[1]) for t in mini_nodes1])
            mini_road2 = LineString([(t[0], t[1]) for t in mini_nodes2])
            road_split = [mini_road1, mini_road2]

            init_pos = nodes[0]
            self.x = init_pos[0]
            self.y = init_pos[1]

            self.angle = self.get_angle(nodes[0], nodes[1])

            self.tot_x.append(self.x)
            self.tot_y.append(self.y)

            i = 0

            for p, mini_road in enumerate(road_split):

                current_length = 0
                if p == 1:

                    self.x = mini_nodes2[0][0]
                    self.y = mini_nodes2[0][1]
                    self.angle = self.get_angle(mini_nodes1[-1], mini_nodes2[0])

                current_pos = [(self.x, self.y)]

                while (current_length < mini_road.length) and i < 1000:
                    distance = self.get_distance(mini_road, self.x, self.y)
                    self.distance = distance

                    self.tot_dist.append(distance)
                    if distance <= 1:
                        self.go_straight()
                        current_pos.append((self.x, self.y))
                        self.speed += 0.3

                    else:
                        angle = -1 + self.angle
                        x = self.speed * np.cos(m.radians(angle)) + self.x
                        y = self.speed * np.sin(m.radians(angle)) + self.y

                        distance_right = self.get_distance(mini_road, x, y)

                        angle = 1 + self.angle
                        x = self.speed * np.cos(m.radians(angle)) + self.x
                        y = self.speed * np.sin(m.radians(angle)) + self.y

                        distance_left = self.get_distance(mini_road, x, y)

                        if distance_right < distance_left:
                            self.turn_right()
                            current_pos.append((self.x, self.y))
                        else:
                            self.turn_left()
                            current_pos.append((self.x, self.y))

                        self.speed -= 0.2

                    current_road = LineString(current_pos)
                    current_length = current_road.length

                    i += 1

            fitness = max(self.tot_dist) * (-1)

            car_path = LineString(zip(self.tot_x, self.tot_y))
            if car_path.is_simple is False:
                fitness = 0

        return fitness, [self.tot_x, self.tot_y]


def point_in_range(a):
    """
    If the point is within 4 units of the edge of the map, return False. Otherwise, return True

    Args:
      a: the point to be checked

    Returns:
      a boolean value.
    """
    map_size = cf.vehicle_env["map_size"]
    if ((4) < a[0] and a[0] < (map_size - 4)) and (
        (4) <= a[1] and a[1] < (map_size - 4)
    ):
        return True
    else:
        return False


def is_invalid_road(points):
    """
    If the road is not simple, or if the road is too sharp, or if the road has less than 3 points, or if
    the last point is not in range, then the road is invalid

    Args:
      points: a list of points that make up the road

    Returns:
      A boolean value.
    """
    nodes = [[p[0], p[1]] for p in points]
    # intp = self.interpolate_road(the_test.road_points)

    in_range = point_in_range(points[-1])

    road = LineString([(t[0], t[1]) for t in nodes])
    invalid = (
        (road.is_simple is False)
        or (is_too_sharp(_interpolate(nodes)))
        or (len(points) < 3)
        or (in_range is False)
    )
    return invalid

# some of this code was taken from https://github.com/se2p/tool-competition-av
def find_circle(p1, p2, p3):
    """
    The function takes three points and returns the radius of the circle that passes through them

    Args:
      p1: the first point
      p2: the point that is the center of the circle
      p3: the point that is the furthest away from the line

    Returns:
      The radius of the circle.
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
        return np.inf

    # Center of circle
    cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
    # print(radius)
    return radius


def min_radius(x, w=5):
    """
    It takes a list of points (x) and a window size (w) and returns the minimum radius of curvature of
    the line segment defined by the points in the window

    Args:
      x: the x,y coordinates of the points
      w: window size. Defaults to 5

    Returns:
      The minimum radius of curvature of the road.
    """
    mr = np.inf
    nodes = x
    for i in range(len(nodes) - w):
        p1 = nodes[i]
        p2 = nodes[i + int((w - 1) / 2)]
        p3 = nodes[i + (w - 1)]
        radius = find_circle(p1, p2, p3)
        if radius < mr:
            mr = radius
    if mr == np.inf:
        mr = 0

    return mr * 3.280839895  # , mincurv


def _interpolate(the_test):
    """
    It takes a list of 2D points and returns a list of 4D points

    Args:
      the_test: The list of points that define the road.

    Returns:
      A list of tuples.
    """

    rounding_precision = 3
    interpolation_distance = 1
    smoothness = 0
    min_num_nodes = 20

    old_x_vals = [t[0] for t in the_test]
    old_y_vals = [t[1] for t in the_test]

    # This is an approximation based on whatever input is given
    test_road_lenght = LineString([(t[0], t[1]) for t in the_test]).length
    num_nodes = int(test_road_lenght / interpolation_distance)
    if num_nodes < min_num_nodes:
        num_nodes = min_num_nodes

    assert len(old_x_vals) >= 2, "You need at leas two road points to define a road"
    assert len(old_y_vals) >= 2, "You need at leas two road points to define a road"

    if len(old_x_vals) == 2:
        # With two points the only option is a straight segment
        k = 1
    elif len(old_x_vals) == 3:
        # With three points we use an arc, using linear interpolation will result in invalid road tests
        k = 2
    else:
        # Otheriwse, use cubic splines
        k = 3

    pos_tck, pos_u = splprep([old_x_vals, old_y_vals], s=smoothness, k=k)

    step_size = 1 / num_nodes
    unew = arange(0, 1 + step_size, step_size)

    new_x_vals, new_y_vals = splev(unew, pos_tck)

    # Return the 4-tuple with default z and defatul road width
    return list(
        zip(
            [round(v, rounding_precision) for v in new_x_vals],
            [round(v, rounding_precision) for v in new_y_vals],
            [-28.0 for v in new_x_vals],
            [8.0 for v in new_x_vals],
        )
    )


def is_too_sharp(the_test, TSHD_RADIUS=47):
    """
    If the minimum radius of the test is greater than the TSHD_RADIUS, then the test is too sharp

    Args:
      the_test: the input road topology
      TSHD_RADIUS: The radius of the circle that is used to check if the test is too sharp. Defaults to
    47

    Returns:
      the boolean value of the check variable.
    """
    if TSHD_RADIUS > min_radius(the_test) > 0.0:
        check = True
        #print("Too sharp")
    else:
        check = False
    return check
