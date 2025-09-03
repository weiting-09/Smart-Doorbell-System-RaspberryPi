import time
import constants
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from firebase_admin import db
from time import sleep

GPIO.setmode(GPIO.BCM)

reader = SimpleMFRC522()

def RFID_job():
    print("Starting RFID job...")
    while True:
        id, text = reader.read_no_block()
        if id is not None:
            print(f"RFID ID: {id}")
        time.sleep(0.5)

        # id, text = reader.read()
        # print(f"RFID ID: {id}, Text: {text}")

        # cardUID, password, start_time, end_time = get_access_settings()
        # if id == cardUID and is_now_in_range(start_time, end_time):
        #     AllowedToEnter("RFID")
        # else:
        #     NotAllowedToEnter("RFID")
        # sleep(1)
        # lcd.clear()

def add_new_RFID():
    while(True):
        try:
            print("請將新的RFID卡片靠近讀取器...")
            id, text = reader.read()
            print(f"新RFID ID: {id}")
            ref = db.reference(f'locks/{constants.lock_id}/RFIDs/{id}')
            if ref.get() is None:
                ref.set({
                    'id': id,
                    'name': "card_" + str(id)
                })
        except Exception as e:
            print(f"讀取RFID時發生錯誤: {e}")
        sleep(1)
        