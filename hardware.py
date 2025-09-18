import RPi.GPIO as GPIO
from LCD import destroy_lcd, setup_lcd
from RFID import stop_add_new_RFID
import constants
from doorbell_chime import play_doorbell_chime

Buzz = None

def setup_initial():
    global Buzz
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(constants.lock, GPIO.OUT)
    GPIO.setup(constants.LED_green, GPIO.OUT)
    GPIO.setup(constants.LED_red, GPIO.OUT)
    GPIO.setup(constants.button, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(constants.Buzzer, GPIO.OUT)

    setup_lcd()

    Buzz = GPIO.PWM(constants.Buzzer, 440)

    GPIO.add_event_detect(
        constants.button, 
        GPIO.FALLING, 
        callback=lambda channel: button_pressed(),
        bouncetime=350
    )
    print("ready to stop add_new_RFID")
    stop_add_new_RFID()
    print("Setup complete.")

def button_pressed():
    if GPIO.input(constants.button) == GPIO.LOW: 
        play_doorbell_chime(Buzz)

def destroy():
    global Buzz
    try:
        Buzz.stop()
        GPIO.output(constants.Buzzer, 1)
        GPIO.cleanup()
        destroy_lcd()
        stop_add_new_RFID()
    except Exception as e:
        print("Error during destroy:", e)