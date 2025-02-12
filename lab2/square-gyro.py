#!/usr/bin/env python3
#square gyroscope
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_2

# Initialize motors and gyro sensor
tank = MoveTank(OUTPUT_B, OUTPUT_C)
gyro = GyroSensor(INPUT_2)

# Reset gyro to zero
gyro.reset()

def turn_90_degrees():
    """Turn the robot by 90 degrees using the gyro."""
    target_angle = gyro.angle + 90  # Add 90 to current angle
    tank.on(37, 0)  # Spin in place
    while gyro.angle < target_angle:
        pass
    tank.off()  # Stop motors

for _ in range(4):
    # Move forward
    tank.on_for_seconds(50, 50, 2)
    
    # Turn 90 degrees
    turn_90_degrees()