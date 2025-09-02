#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import ColorSensor, GyroSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.button import Button
from time import sleep, time
from math import pi

class Robot:

	def __init__(self):
		# Initialize devices
		self.tank = MoveTank(OUTPUT_B, OUTPUT_C)

		# Two ultrasonic sensors: side and back
		self.ultrasonic_side = UltrasonicSensor(INPUT_1)
		self.gyro_sensor = GyroSensor(INPUT_2)
		self.color_sensor = ColorSensor(INPUT_3)
		self.ultrasonic_back = UltrasonicSensor(INPUT_4)

		self.button = Button()

		# Variables for parking
		self.duration = 0

		# Reset and calibrate gyro to avoid drift
		self.gyro_sensor.reset()
		sleep(0.5)
		self.gyro_sensor.calibrate()



	# Function to turn using gyro
	def turn_degrees(self, degrees, speed=20):
		print("Turning ", degrees, " degrees")
		self.gyro_sensor.reset()
		sleep(0.5)

		target_angle = self.gyro_sensor.angle + degrees
		if degrees > 0: # Turn right
			self.tank.on(speed, -speed)
		else: # Turn left
			self.tank.on(-speed, speed)
		
		while abs(self.gyro_sensor.angle - target_angle) > 5: # Wait until turn is complete
			pass # Maybe improve with sleep(0.01)

		self.tank.off()



	# Function to select parking type
	def select_parking_type(self):
		print("Select Parking Mode:")
		print("Left button: Perpendicular Parking")
		print("Right button: Parallel Parking")
		print("Up button: Angled Parking (45 degrees)")

		while True:
			if self.button.left:
				print("Perpendicular Parking Selected")
				return "perpendicular"
			elif self.button.right:
				print("Parallel Parking Selected")
				return "parallel"
			elif self.button.up:
				print("Angled Parking Selected")
				return "angled"
			sleep(0.1)



	# Function to find parking space
	def find_parking_space(self, parking_type):
		print("Scanning for parking space...")

		# Required dimensions
		if parking_type == "perpendicular":
			required_width = 20
			required_depth = 30
		elif parking_type == "parallel":
			required_width = 30
			required_depth = 20
		elif parking_type == "angled":
			required_width = 17
			required_depth = 27
		else:
			print("Unknown parking type")
			return False
		
		found_space = False
		start_time = None

		# Calculation for space covered per second
		wheel_speed = 20
		wheel_diameter = 5.6
		wheel_circumference = pi * wheel_diameter
		max_motor_rpm = 170
		motor_power_cm_per_sec = max_motor_rpm * wheel_circumference / 60
		speed_cm_per_sec = motor_power_cm_per_sec * wheel_speed / 100

		self.tank.on(wheel_speed, wheel_speed) # Start moving forward
		
		# Scan for parking space
		while True:
			distance = self.ultrasonic_side.distance_centimeters

			if distance >= required_depth:
				if not found_space:
					found_space = True
					start_time = time()
					print("Open space started")
			else:
				if found_space:
					end_time = time()
					self.duration = end_time - start_time
					width = self.duration * speed_cm_per_sec

					print("Open space ended, width: ", width, " cm")

					if width >= required_width:
						self.tank.off()
						print("Suitable parking space found!")
						return True
					else:
						print("Space too small")
						found_space = False
						start_time = None

			
			if self.button.enter: # Cancel search manually
				self.tank.off()
				print("Search cancelled")
				return False
			
			sleep(0.05)



	# Function for Perpendicular Parking
	def perpendicular_parking(self):
		time_start = time()
		while time() - time_start < self.duration:
			self.tank.on(-20, -20)
		self.tank.off()

		self.turn_degrees(90)
		self.reverse_into_parking()



	# Function for Parallel Parking
	def parallel_parking(self):		
		self.turn_degrees(45) # Turn
		sleep(0.5)

		if self.ultrasonic_side.distance_centimeters < 10:
			print("Too close to wall, adjusting position...")
			self.tank.on_for_seconds(10, 10, 0.5)
			self.turn_degrees(-45)
			self.tank.on_for_seconds(10, 10, 0.5)
			self.turn_degrees(45)

		self.reverse_into_parking()
		self.turn_degrees(-45, 10) # Straighten car
		self.tank.on_for_seconds(10, 10, 1)



	# Function for Angled Parking
	def angled_parking(self):
		self.tank.on_for_seconds(20, 20, 1.5) # Move a bit forward
		time_start = time()
		while time() - time_start < self.duration / 2:
			self.tank.on(-20, -20)
		self.tank.off()

		self.turn_degrees(45)
		sleep(0.5)
		self.reverse_into_parking()



	# Reverse parking with touch sensor
	def reverse_into_parking(self):
		print("Reversing into parking slot...")

		# Reverse until at 5 cm of the wall
		print("Distance to wall: ", self.ultrasonic_back.distance_centimeters)
		while self.ultrasonic_back.distance_centimeters > 6:
			self.tank.on(-20, -20)

		self.tank.off()
		# print("Reached end of parking slot, adjusting parking.")

		# Fine-tune if too close
		# distance = self.ultrasonic_back.distance_centimeters
		# if distance < 3:
		# 	print("Too close to wall, back of slightly...")
		# 	self.tank.on_for_seconds(10, 10, 0.5)
		# 	sleep(1)
		# 	self.tank.on_for_seconds(-10, -10, 0.5)

		# Align using side ultrasonic
		# side_distance = self.ultrasonic_side.distance_centimeters
		# if side_distance < 10:
		# 	print("Adjusting left...")
		# 	self.tank.on_for_seconds(-10, 10, 0.3) # Move slightly left
		# elif side_distance > 30:
		# 	print("Adjusting right...")
		# 	self.tank.on_for_seconds(10, -10, 0.3) # Move slightly right

		print("Parked successfully!")



	# Exit parking space
	def exit_parking(self):
		print("Waiting to exit")
		while not self.button.enter: # Wait until button is pressed
			sleep(0.1)

		print("Exiting parking space...")
		self.tank.on_for_seconds(20, 20, 1)
		self.turn_degrees(-90) # Turn left
		self.tank.on(30, 30) # COntinue driving
		print("Exited parking successfully!")



	# Function to follow traffic rules
	def follow_traffic_rules(self):
		speed = 30
		color = "green"
		while True:
			if color != "red":
				self.tank.on(speed, speed)

			if color != "red" and self.color_sensor.color == 5:
				color = "red"
				print("Red light detected, stopping...")
				self.tank.off()
			if color != "green" and self.color_sensor.color == 3:
				color = "green"
				speed = 30
				print("Green light detected, continue driving")
			if color != "yellow" and self.color_sensor.color == 4:
				color = "yellow"
				speed = 15
				print("Yellow light detected, continue driving slowly")
			
			if self.button.enter: # Check if middle button is pressed for parking
				print("Parking mode activated!")
				self.tank.off()
				return # Exit traffic mode



	def run(self):
		self.follow_traffic_rules()

		parking_type = self.select_parking_type()

		if self.find_parking_space(parking_type):
			if parking_type == "perpendicular":
				self.perpendicular_parking()
			elif parking_type == "parallel":
				self.parallel_parking()
			elif parking_type == "angled":
				self.angled_parking()

			sleep(10)
			self.exit_parking()



if __name__ == "__main__":
	robot = Robot()
	robot.run()

## TODO - swap touch sensor with ultrasonic sensor (at the back) fix reverse a bit in angled before reverse into parking
## in parallel if it is too close when turing the first time it crashes with the wall.