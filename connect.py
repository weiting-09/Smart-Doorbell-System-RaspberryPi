import secrets
import string

def generate_safe_id():
    length=6
    safe_id = ""
    
    # 大小寫字母 + 數字 + 安全符號
    chars = string.ascii_letters + string.digits + "@#$%^&*_-+="
    for _ in range(length):
        safe_id += secrets.choice(chars)

    return safe_id
