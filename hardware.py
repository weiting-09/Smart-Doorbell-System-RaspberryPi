import RPi.GPIO as GPIO
from LCD import destroy_lcd, setup_lcd
import constants
from doorbell_chime import play_doorbell_chime

Buzz = None

def setup_hardware():
    global Buzz
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(constants.lock, GPIO.OUT)
    GPIO.setup(constants.LED_green, GPIO.OUT)
    GPIO.setup(constants.LED_red, GPIO.OUT)
    GPIO.setup(constants.button, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(constants.Buzzer, GPIO.OUT)

    setup_lcd()

    Buzz = GPIO.PWM(constants.Buzzer, 440)

    GPIO.add_event_detect(constants.button, GPIO.FALLING, 
                        callback=lambda channel: button_pressed(Buzz),bouncetime=350)
    print("Hardware setup complete.")

def button_pressed(channel):
    if GPIO.input(constants.button) == GPIO.LOW:  # 真的按下
        play_doorbell_chime(Buzz)

def destroy():
    global Buzz
    Buzz.stop()
    GPIO.output(constants.Buzzer, 1)
    GPIO.cleanup()
    destroy_lcd()