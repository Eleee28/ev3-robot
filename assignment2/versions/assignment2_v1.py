#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, GyroSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from time import sleep

# Initialize devices
tank = MoveTank(OUTPUT_B, OUTPUT_C)
touch_sensor = TouchSensor(INPUT_1)
gyro_sensor = GyroSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_3)
ultrasonic_sensor = UltrasonicSensor(INPUT_4)

# Reset and calibrate gyro to avoid drift
gyro_sensor.reset()
gyro_sensor.calibrate()

# Function to turn using gyro
def turn_degrees(degrees, speed=20):
	gyro_sensor.reset()
	if degrees > 0: # Turn right
		tank.on(speed, -speed)
	else: # Turn left
		tank.on(-speed, speed)
	
	while abs(gyro_sensor.angle) < abs(degrees): # Wait until turn is complete
		pass

	tank.off()

# Function to find parking space
def find_parking_space():
	# Scan for parking space
	while True:
		tank.on(30,30) # Move forward
		if ultrasonic_sensor.distance_centimeters > 30:
			tank.off()
			print("Potential parking space!")
			sleep(1)
		
			# Check space is empty
			tank.on_for_seconds(10, 10, 1) # Move a bit in the space
			sleep(1)

			if ultrasonic_sensor.distance_centimeters > 30:
				print("Parking slot is empty!")
			else:
				print("Parking slot is occupied!")

# Reverse parking with touch sensor
def reverse_into_parking():
	while not touch_sensor.is_pressed: # Reverse until touch activated
		tank.on(-20,-20)

	tank.off()
	print("Touch sensor activated, adjusting parking.")

    # Fine-tune if too close
	if ultrasonic_sensor.distance_centimeters < 5:
		tank.on_for_seconds(10, 10, 0.5)
		sleep(1)
		tank.on_for_seconds(-10, -10, 0.5)

	print("Parked successfully!")

# Exit parking space
def exit_parking():
	print("Exiting parking space...")
	tank.on_for_seconds(20, 20, 1)
	turn_degrees(-90) # Turn left
	tank.on(30, 30) # COntinue driving
	print("Exited parking successfully!")

# Function to follow traffic rules
def follow_rules():
	while True:
		tank.on(30, 30)

		if color_sensor.color == 1: # maybe it is 5
			print("Red light detected, stopping...")
			tank.off()
			sleep(3)
		elif color_sensor.color == 7: # maybe 3
			print("Green light detected, continue driving")

# Main Execution Flow
if __name__ == "__main__":
	if find_parking_space():
		turn_degrees(90)
		reverse_into_parking()
		sleep(5)
		exit_parking()
	follow_rules()
