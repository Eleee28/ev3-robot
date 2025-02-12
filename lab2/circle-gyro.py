#!/usr/bin/env python3
# circle giroscope
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_2

# Initialize motors and gyro sensor
tank = MoveTank(OUTPUT_B, OUTPUT_C)
gyro = GyroSensor(INPUT_2)

# Reset gyro to zero
gyro.reset()

def rotate_on_spot():
    """Rotate the robot on the spot to complete a 360-degree turn."""
    target_angle = gyro.angle + 360
    tank.on(50, -50)  # Opposite wheel directions for in-place rotation
    while gyro.angle < target_angle:
        pass
    tank.off()

def travel_in_circle():
    """Move the robot in a circle by setting different wheel speeds."""
    tank.on_for_degrees(50, 25, 3080)  # One motor slower to create a circular path
    tank.off()

print("Rotating on the spot:")
rotate_on_spot()
print("Traveling in a circle:")
travel_in_circle()