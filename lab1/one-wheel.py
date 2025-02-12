#!/usr/bin/env python3
# one wheel motor
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C

# Initialize the motors
tank = MoveTank(OUTPUT_B, OUTPUT_C)

# Loop through four sides to make a square
for _ in range(4):
    # Move forward
    tank.on_for_seconds(50, 50, 2)  # Move both wheels at speed 50 for 2 seconds
    
    # Turn right by moving one wheel only (B moves, C is static)
    tank.on_for_seconds(39, 0, 1)  # Adjust time until it turns approximately 90 degrees