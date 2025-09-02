#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from time import time, sleep

def measure_speed(power=20, distance_cm=50):
    tank = MoveTank(OUTPUT_B, OUTPUT_C)

    input(f"Place the robot at the start line and press Enter to begin...")

    print(f"Driving at power {power}% to cover {distance_cm} cm...")

    start_time = time()
    tank.on(power, power)

    # Wait until the robot is manually stopped at 50 cm mark
    input("Press Enter once the robot reaches the 50 cm mark...")
    tank.off()
    end_time = time()

    duration = end_time - start_time
    speed = distance_cm / duration

    print(f"\nTime taken: {duration:.2f} seconds")
    print(f"Calculated speed: {speed:.2f} cm/s at {power}% power")

if __name__ == "__main__":
    measure_speed()
