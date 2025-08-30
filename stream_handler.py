from firebase_admin import db
import RPi.GPIO as GPIO
from constants import lock_id
from lock import lock_the_door, unlock_the_door

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
def stream_handler_listener():
    status_ref = db.reference('locks/' + lock_id )
    status_ref.listen(stream_handler)
