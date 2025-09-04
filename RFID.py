import time
from access_control import allowed_to_enter, not_allowed_to_enter
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
        print("請將RFID卡片靠近讀取器...")
        id, text = reader.read()
        if id is not None:
            print(f"RFID ID: {id}")
        time.sleep(0.5)
        ref = db.reference(f'locks/{constants.lock_id}/RFIDs/')
        if ref.get() and str(id) in ref.get().keys():
            print("RFID recognized, allowed to enter.")
            allowed_to_enter(method="RFID")
        else:
            print("RFID not recognized, not allowed to enter.")
            not_allowed_to_enter(method="RFID")

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
        