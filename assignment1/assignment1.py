#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import TouchSensor, ColorSensor, GyroSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.button import Button
from ev3dev2.display import Display
import ev3dev2.fonts as fonts
import time

# Initialize devices
tank = MoveTank(OUTPUT_B, OUTPUT_C)
touch = TouchSensor(INPUT_1)
gyro = GyroSensor(INPUT_2)
color = ColorSensor(INPUT_3)
ultrasonic = UltrasonicSensor(INPUT_4)
btn = Button()
screen = Display()

# Reset gyroscope
gyro.reset()

# Define unit
UNIT_DISTANCE = 100

def display_message(message):
    """Display a message on the EV3 screen"""
    screen.clear()
    screen.text_grid(message, 3, 3, font=fonts.load('ncenB18')) # Display message with chosen font
    screen.update()

def wait_for_button_press():
    """Wait for any button to be pressed before proceeding"""
    while not btn.any():
        pass

def move_forward_until_obstacle():
    """Move forward until ultrasonic sensor detects obstacle (distance: 25cm)"""
    tank.on(50, 50) # Move forward, speed: 50
    while ultrasonic.distance_centimeters > 25:
        pass
    tank.off() # Stop when obstacle is detected

def turn_degrees(angle):
    """Turn robot an angle using the gyroscope"""
    # Positive angle to turn right, negative to turn left
    target_angle = gyro.angle + angle
    turn_speed = 30 if angle > 0 else -30 # Direction of turn
    tank.on(turn_speed, -turn_speed) # Rotate on spot
    while abs(gyro.angle - target_angle) > 5: # Buffer for accuracy
        pass
    tank.off()

def move_forward_units(units):
    """Move forward a number of units"""
    tank.on_for_degrees(50, 50, units * UNIT_DISTANCE) # Move number of units at speed of 50

def move_forward_until_dark():
    """Move forward until color sensor detects dark surface"""
    tank.on(50, 50) # Move forward, speed: 50
    while color.reflected_light_intensity > 5: # Range (0-100), 10 considers floor is dark
        pass
    tank.off() # Stop when obstacle is detected

def move_backward_until_touch():
    """Move Backward until touch sensor is pressed"""
    tank.on(-40, -40) # Reverse at slower speed
    while not touch.is_pressed:
        pass
    tank.off()

# Main Flow
display_message("Assignment 1")
wait_for_button_press()
screen.clear()
screen.update()
move_forward_until_obstacle()
turn_degrees(180)
move_forward_units(20)
turn_degrees(-90)
move_forward_until_dark()
tank.off()
time.sleep(1) # Make the stop visual
turn_degrees(-90)
move_backward_until_touch()