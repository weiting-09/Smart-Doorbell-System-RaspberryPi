import queue
import time
from LCD import LCD_display_job, clear_lcd_and_show_prompt
from access_control import allowed_to_enter, not_allowed_to_enter
import constants
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from firebase_admin import db

GPIO.setmode(GPIO.BCM)
reader = SimpleMFRC522()

rfid_queue = queue.Queue()
REGISTER_TIMEOUT = 15

def rfid_reader_job():
    while True:
        id = reader.read_id()
        if id:
            print(f"[Reader] 感應到卡片 {id}")
            rfid_queue.put(id)
        time.sleep(1.5)

def rfid_controller_job():
    ref = db.reference(f'locks/{constants.lock_id}/RFIDs/')

    while True:
        id = rfid_queue.get()

        if is_register_mode():
            current_mode = "register"
        else:
            current_mode = "verify"

        print("current_mode:", current_mode)

        if current_mode == "verify":
            print(f"[Verify] card_{id}")
            if ref.get() and str(id) in ref.get().keys():
                print("RFID recognized, allowed to enter.")
                allowed_to_enter(method="RFID")
            else:
                print("RFID not recognized, not allowed to enter.")
                not_allowed_to_enter(method="RFID")

        elif current_mode == "register":
            print(f"[Register] try to register_{id}")
            ref_card = ref.child(str(id))
            if ref_card.get() is None:
                ref_card.set({
                    'id': id,
                    'name': "card_" + str(id)
                })
                print("Card added successfully")
            else:
                print("This card already exists.")
            stop_add_new_RFID() 

        rfid_queue.task_done()
        clear_lcd_and_show_prompt()

def add_new_RFID():
    print(f"切換至[Register]，請在 {REGISTER_TIMEOUT} 秒內刷卡...")
    
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        LCD_display_job(line1="please tap card", 
                        line2=f"in {int(REGISTER_TIMEOUT - elapsed)}s")
        if  elapsed > REGISTER_TIMEOUT:
            print("超過時間，新增模式自動結束")
            stop_add_new_RFID()
            return
        elif is_register_mode() == False:
            clear_lcd_and_show_prompt()
            return
        time.sleep(0.5)

def stop_add_new_RFID():
    db.reference(f'locks/{constants.lock_id}/RFIDs/add_new_RFID').set(False)
    print("新增模式已結束")

def is_register_mode():
    return db.reference(f'locks/{constants.lock_id}/RFIDs/add_new_RFID').get()
