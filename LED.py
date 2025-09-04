import RPi.GPIO as GPIO
import constants

def turn_on_red_led():
    print("Red LED ON")
    GPIO.output(constants.LED_red, GPIO.HIGH)

def turn_off_red_led():
    print("Red LED OFF")
    GPIO.output(constants.LED_red, GPIO.LOW)

def turn_on_green_led():
    print("Green LED ON")
    GPIO.output(constants.LED_green, GPIO.HIGH)

def turn_off_green_led():
    print("Green LED OFF")
    GPIO.output(constants.LED_green, GPIO.LOW)