import math


class KinematicModel:
    '''
    The KinematicModel class updates the position, speed, and yaw angle of a vehicle based on steering,
    acceleration, and time.
    '''
    def __init__(self, x, y, yaw, speed):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.speed = speed

    def update(self, steering, acceleration, delta_time, speed):
        """
        This function updates the position, speed, and yaw angle of a vehicle based on the steering,
        acceleration, delta time, and current speed.
        
        Args:
          steering: The steering input from the driver or controller, which determines the direction the
        vehicle should turn.
          acceleration: The rate of change of the speed of the object. It can be positive (accelerating) or
        negative (decelerating).
          delta_time: The time elapsed since the last update of the vehicle's position and speed.
          speed: The current speed of the vehicle.
        """
        # Calculate the new yaw angle
        self.yaw += steering * delta_time

        self.speed = speed

        # Calculate the new speed
        self.speed += acceleration * delta_time

        # Calculate the new x and y position
        self.x += self.speed * math.cos(self.yaw) * delta_time
        self.y += self.speed * math.sin(self.yaw) * delta_time
