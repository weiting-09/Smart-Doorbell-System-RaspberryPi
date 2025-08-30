import secrets
import string
from firebase_admin import db
import constants 

def connect_to_smartPhone():
    print("Connecting to smartphone...")
    connect_id = generate_connect_id()
    db.reference('connect/' + constants.lock_id).set(connect_id)

def generate_connect_id():
    length=6
    connect_id = ""
    
    # 大小寫字母 + 數字 + 安全符號
    chars = string.ascii_letters + string.digits + "@#$%^&*_-+="
    for _ in range(length):
        connect_id += secrets.choice(chars)

    return connect_id

#取得 Raspberry Pi CPU 序號
def get_raspberryPi_cpu_id():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("Serial"):
                    serial = line.strip().split(":")[1].strip()
                    print("This Raspberry Pi's ID:", serial)
                    return serial
    except FileNotFoundError:
        print("Cannot get Raspberry Pi ID")
        return None
    