import threading
from RFID import add_new_RFID
from firebase_admin import db
import RPi.GPIO as GPIO
from lock import lock_the_door, unlock_the_door
import constants

rfid_thread = None

def stream_handler(event):
    global rfid_thread
    if event.path == "/":
        print("初始化資料")
    else:
        print("資料變更：")
        print("Path:", event.path)
        print("Data:", event.data)
        
        if event.path == "/isOpened":
            if event.data:
                unlock_the_door()
                print("門已解鎖")
            else:
                lock_the_door()
                print("門已上鎖")

        elif event.path == "/RFIDs/add_new_RFID":
            if event.data:
                print("開始新增RFID")
                rfid_thread = threading.Thread(target=add_new_RFID)
                rfid_thread.daemon = True  # 主程式結束時會自動結束
                rfid_thread.start()

            else:
                print("結束新增RFID")
                if rfid_thread and rfid_thread.is_alive():
                    rfid_thread.join(timeout=2)

# 監聽欄位變化
def stream_handler_listener(lock_id):
    constants.lock_id = lock_id
    status_ref = db.reference(f'locks/{lock_id}')
    set_lock_default_data(status_ref)
    status_ref.listen(stream_handler)

def set_lock_default_data(status_ref):
    current_data = status_ref.get()
    if current_data is None:
        default_data = {
            # TODO: 加入lock預設欄位
            'isOpened': False,
            'RFIDs': {
                'add_new_RFID': False
            },
            # 'passwords': {},
            # 'onlock_logs': {}
        }
        status_ref.set(default_data)
        print(f"lock原本不存在，已建立預設資料")
