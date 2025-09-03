from RFID import RFID_job
import firebase_admin
from firebase_admin import credentials, db
from time import time, sleep
import RPi.GPIO as GPIO
import multiprocessing
import threading
from hardware import setup_hardware
from numpad import keyboard_input_job
from stream_handler import stream_handler_listener
import constants
from connect import get_raspberryPi_cpu_id

# 初始化 Firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-doorbell-system-b85c7-default-rtdb.firebaseio.com/'
})

def main():
    setup_hardware()
    constants.lock_id = get_raspberryPi_cpu_id()
    p = multiprocessing.Process(target=stream_handler_listener, args=(constants.lock_id,))
    p.start()

    try:
        threading.Thread(target=keyboard_input_job).start()
        threading.Thread(target=RFID_job).start()
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