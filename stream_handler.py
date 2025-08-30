from firebase_admin import db
import RPi.GPIO as GPIO
from lock import lock_the_door, unlock_the_door
import constants

def stream_handler(event):
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
        }
        status_ref.set(default_data)
        print(f"lock原本不存在，已建立預設資料")
