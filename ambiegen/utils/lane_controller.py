import math

class LaneController:
    """
    The LaneController class implements a controller for a vehicle to follow a given set of waypoints
    while adjusting speed and steering angle based on the current position and orientation of the
    vehicle.
    The LaneController class implements a controller for a lane with various parameters such as speed
    and waypoints.
    """
    def __init__(self, waypoints, speed):
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.done = False
        self.max_steering = math.pi
        #self.cutoff_frequency = 3
        self.previous_yaw = 0
        self.window = 10
        self.point_limit = 10
        self.speed_increment = 1
        self.max_speed = 30
        self.speed = speed
        self.min_speed = 8

    def control(self, x, y, yaw, speed):
        """
        This function calculates the steering angle and speed of a vehicle based on its current position
        and the closest waypoint.
        
        Args:
          x: The current x-coordinate of the vehicle
          y: The "y" parameter in the "control" function is the current y-coordinate of the vehicle's
        position.
          yaw: Yaw is the current orientation of the vehicle, measured in radians from the positive
        x-axis.
          speed: The current speed of the vehicle.
        
        Returns:
          a tuple containing the steering angle, speed, closest distance to the next waypoint, and a
        boolean indicating whether the vehicle has reached the end of the waypoints.
        """
        # Find the next waypoint
        closest_distance = float('inf')
        closest_waypoint = self.current_waypoint
        
        for i, waypoint in enumerate(self.waypoints[self.current_waypoint:self.point_limit]):
            self.point_limit = min(len(self.waypoints)-1,self.current_waypoint + self.window)
            distance = math.sqrt((x - waypoint[0])**2 + (y - waypoint[1])**2)
            if distance < closest_distance:
                closest_distance = distance
                #i = min(i, 10)
                closest_waypoint = i + self.current_waypoint
        self.current_waypoint = closest_waypoint

        # Calculate the target yaw based on the waypoint
        if self.current_waypoint >=  len(self.waypoints) - 4:
            self.done = True
            steering = 0
        else:

            dx = self.waypoints[self.current_waypoint+1][0] - x
            dy = self.waypoints[self.current_waypoint+1][1] - y
            
            target_yaw = math.atan2(dy, dx)
            if dy > 0:# and dx < 0:
                target_yaw -= 2*math.pi
            
            self.previous_yaw = target_yaw

            # Calculate the steering angle
            steering = target_yaw - yaw

            self.speed = speed
            
            if abs(target_yaw - yaw) < 0.4: # if the vehicle is going straight
                self.speed += self.speed_increment
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
            elif abs(target_yaw - yaw) > 1.2:
                self.speed -= self.speed_increment/2
                if self.speed <  self.min_speed:
                    self.speed = self.min_speed

            # Limit the steering angle
            
            if steering > math.pi:
                steering = steering - 2*math.pi
            elif steering < -math.pi:
                steering = steering + 2*math.pi

            steering = min(steering, self.max_steering)
            steering = max(steering, -self.max_steering)

        return steering, self.speed, closest_distance, self.done




