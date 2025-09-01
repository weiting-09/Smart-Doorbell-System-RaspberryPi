import RPi.GPIO as GPIO
from constants import lock

def lock_the_door():
    GPIO.output(lock, GPIO.LOW)#LOW為上鎖
    print("locked (LOW)")

def unlock_the_door():
    GPIO.output(lock, GPIO.HIGH)#HIGH為解鎖
    print("unlock (HIGH)")

# def allowed_to_enter(method="unknown"):
#     GPIO.output(LED_green, GPIO.HIGH)
#     lcd.clear()
#     lcd.write_string("Welcome")
#     sleep(1)
#     GPIO.output(LED_green, GPIO.LOW)
#     lcd.clear()
#     update_lock_status(True)
#     log_access("allowed", method)
#     #解鎖紀錄

# def not_allowed_to_enter(method="unknown"):
#     GPIO.output(LED_red, GPIO.HIGH)
#     lcd.clear()
#     lcd.write_string("not allowed")
#     lcd.cursor_pos = (1, 7)
#     lcd.write_string("to enter")
#     sleep(1)
#     GPIO.output(LED_red, GPIO.LOW)
#     lcd.clear()
#     update_lock_status(False)
#     log_access("denied", method)
#     #解鎖紀錄