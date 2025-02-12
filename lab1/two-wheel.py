#!/usr/bin/env python3
# two wheels motor
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C

# Initialize the motors
tank = MoveTank(OUTPUT_B, OUTPUT_C)

# Loop through four sides to make a square
for _ in range(4):
    # Move forward
    tank.on_for_seconds(50, 50, 2)  # Both wheels move at speed 50
    
    # Turn right by moving both wheels at different speeds
    tank.on_for_seconds(50, 12, 1)  # Adjust speeds and time until it turns 90 degrees