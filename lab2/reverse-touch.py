#!/usr/bin/env python3
# reversing with touch sensor
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor import INPUT_2, INPUT_1

# Initialize motors, gyro sensor and touch sensor
tank = MoveTank(OUTPUT_B, OUTPUT_C)
gyro = GyroSensor(INPUT_2)
touch = TouchSensor(INPUT_1)

# Reset gyro to zero
gyro.reset()


def reverse_and_turn_180():
    """Reverse and turn 180 degrees upon touch sensor activation."""
    # Reverse
    tank.on_for_seconds(-50, -50, 1)  # Move backward for 1 second
    
    # Turn 180 degrees using gyro
    target_angle = gyro.angle + 180
    tank.on(50, -50)  # Rotate on the spot
    while gyro.angle < target_angle:
        pass
    tank.off()

print("Waiting for touch sensor activation...")
while True:
    tank.on(50, 50)  # Move forward
    if touch.is_pressed:
        print("Touch detected! Reversing and turning...")
        reverse_and_turn_180()
        break