import queue
import time
from access_control import allowed_to_enter, not_allowed_to_enter
import constants
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from firebase_admin import db
from time import sleep

GPIO.setmode(GPIO.BCM)

reader = SimpleMFRC522()

# 建立全域 Queue
rfid_queue = queue.Queue()

# Producer: RFID Reader
def rfid_reader_job():
    while True:
        id = reader.read_id()
        if id:
            print(f"[Reader] 感應到卡片 {id}")
            rfid_queue.put(id)   # 丟進 Queue
        time.sleep(0.5)  # 避免 CPU 過高

def RFID_job():
    print("Starting RFID job...")
    while True:
        print("請將RFID卡片靠近讀取器...")
        id = rfid_queue.get()
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

#TODO: 增加計時器，未在一定時間內新增完成即關閉新增功能
def add_new_RFID():
    ref = db.reference(f'locks/{constants.lock_id}/RFIDs/')
    while(True):
        try:
            print("請將新的RFID卡片靠近讀取器...")
            id = rfid_queue.get()
            if id:
                ref_card = ref.child(str(id))
                if ref_card.get() is None:
                    print(f"新RFID ID: {id}")
                    ref_card.set({
                        'id': id,
                        'name': "card_" + str(id)
                    })
                else:
                    print("This card already exists.")
                stop_add_new_RFID()
                return
            else:
                print("id is None")
        except Exception as e:
            print(f"讀取RFID時發生錯誤: {e}")
        sleep(1)

def stop_add_new_RFID():
    db.reference(f'locks/{constants.lock_id}/RFIDs/add_new_RFID').set(False)