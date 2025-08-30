import firebase_admin
from firebase_admin import credentials
from time import time, sleep
import RPi.GPIO as GPIO
import multiprocessing
import threading
from numpad import keyboard_input_job
from stream_handler import stream_handler_listener
import constants

# 初始化 Firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-doorbell-system-b85c7-default-rtdb.firebaseio.com/'
})

GPIO.setmode(GPIO.BCM)

GPIO.setup(constants.lock, GPIO.OUT)
#GPIO.setup(constants.LED_green, GPIO.OUT)
#GPIO.setup(constants.LED_red, GPIO.OUT)
#GPIO.setup(constants.button, GPIO.IN, GPIO.PUD_UP)
#GPIO.setup(constants.Buzzer, GPIO.OUT)

def main():
    p = multiprocessing.Process(target=stream_handler_listener)
    p.start()

    try:
        threading.Thread(target=keyboard_input_job).start()
        while True:
            # db.reference('locks/lock_001/status').set(True)
            # sleep(1)
            # db.reference('locks/lock_001/status').set(False)
            sleep(1)
            
    except KeyboardInterrupt:
        print("停止監聽")
        p.terminate()
        p.join()
        print("監聽已停止")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()