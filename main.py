import firebase_admin
from firebase_admin import credentials, db
from time import time, sleep
import RPi.GPIO as GPIO
import threading
import multiprocessing


# 初始化 Firebase
cred = credentials.Certificate("function-test-firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://function-test-4bdd0-default-rtdb.firebaseio.com/'
})


def stream_handler(event):
    print("資料變更：")
    print("Path:", event.path)
    print("Data:", event.data)

# 監聽 status 欄位
def stream_handler_listener():
    status_ref = db.reference('locks/lock_001/status')
    status_ref.listen(stream_handler)


def main():
    p = multiprocessing.Process(target=stream_handler_listener)
    p.start()

    try:
        while True:
            db.reference('locks/lock_001/status').set(True)
            sleep(1)
            db.reference('locks/lock_001/status').set(False)
            sleep(1)
            
    except KeyboardInterrupt:
        print("停止監聽")
        p.terminate()
        p.join()
        print("監聽已停止")
    # finally:
    #     GPIO.cleanup()

if __name__ == "__main__":
    main()