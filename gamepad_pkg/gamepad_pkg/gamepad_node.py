#!/usr/bin/env python3

import pygame
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys

class ControllerPublisher(Node):
    def __init__(self):  # Fix the method name to __init__
        super().__init__('gamepad_node')
        
        # Publisher for the Twist message
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        # Initialize pygame and joystick
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            self.get_logger().error("No joystick connected.")
            sys.exit(1)

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.get_logger().info(f"Controller connected: {self.joystick.get_name()}")
        
        # Timer to repeatedly check joystick input
        self.create_timer(0.1, self.joystick_callback)

    def joystick_callback(self):
        # Process events (necessary for pygame to update)
        pygame.event.pump()

        # Get joystick axes (assuming axis 0 is left-right and axis 1 is forward-backward)
        linear_axis_Y = self.joystick.get_axis(0)  # Typically left stick Y-axis
        linear_axis_X = self.joystick.get_axis(1)  # Typically left stick X-axis
        angular_axis_Z = self.joystick.get_axis(3)

        # Invert axis if necessary (depends on controller setup)
        linear_velocity_Y = -linear_axis_Y *  1.0  # Adjust scale as needed
        linear_velocity_X = linear_axis_X *   1.0  # Adjust scale as needed
        angular_velocity_Z = angular_axis_Z * 1.0

        # Create a Twist message
        twist = Twist()
        twist.linear.x = -linear_velocity_X
        twist.linear.y = 0.0
        twist.angular.z = angular_velocity_Z
        if(abs(linear_velocity_X) < 0.01 ):
            twist.linear.x = 0.0
        if(abs(linear_velocity_Y) < 0.01):
            twist.linear.y = 0.0
        if(abs(angular_velocity_Z) < 0.01):
            twist.angular.z=0.0

        # Publish the Twist message to cmd_vel
        self.publisher_.publish(twist)

        # self.get_logger().info(f"Linear Velocity: {linear_velocity}, Angular Velocity: {angular_velocity}")

def main(args=None):
    rclpy.init(args=args)
    
    try:
        controller_publisher = ControllerPublisher()
        rclpy.spin(controller_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
