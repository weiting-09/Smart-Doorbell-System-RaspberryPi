import secrets
import string

def generate_safe_id():
    length=6
    safe_id = ""
    
    # 大小寫字母 + 數字 + 安全符號
    chars = string.ascii_letters + string.digits + "@#$%^&*_-+="
    for _ in range(length):
        safe_id += secrets.choice(chars)
    
    get_raspberry_pi_id()

    return safe_id

#取得 Raspberry Pi CPU 序號
def get_raspberry_pi_id():
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
    