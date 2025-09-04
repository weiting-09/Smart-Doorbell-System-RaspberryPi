import RPi.GPIO as GPIO
from constants import lock

def lock_the_door():
    GPIO.output(lock, GPIO.LOW)#LOW為上鎖
    print("locked (LOW)")

def unlock_the_door():
    GPIO.output(lock, GPIO.HIGH)#HIGH為解鎖
    print("unlock (HIGH)")