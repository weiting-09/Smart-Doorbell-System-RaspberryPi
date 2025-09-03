import RPi.GPIO as GPIO
import constants
from doorbell_chime import play_doorbell_chime

def setup_hardware():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(constants.lock, GPIO.OUT)
    #GPIO.setup(constants.LED_green, GPIO.OUT)
    #GPIO.setup(constants.LED_red, GPIO.OUT)
    GPIO.setup(constants.button, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(constants.Buzzer, GPIO.OUT)

    Buzz = GPIO.PWM(constants.Buzzer, 440)

    GPIO.add_event_detect(constants.button, GPIO.FALLING, 
                        callback=lambda channel: play_doorbell_chime(Buzz),bouncetime=350)