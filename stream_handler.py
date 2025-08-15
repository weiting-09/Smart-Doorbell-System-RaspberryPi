from firebase_admin import db

def stream_handler(event):
    print("資料變更：")
    print("Path:", event.path)
    print("Data:", event.data)

# 監聽 status 欄位
def stream_handler_listener():
    status_ref = db.reference('locks/lock_001/status')
    status_ref.listen(stream_handler)
