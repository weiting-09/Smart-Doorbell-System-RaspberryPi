from datetime import datetime
import time
from evdev import InputDevice, ecodes, categorize
from connect import connect_to_smartphone
from firebase_admin import db
import constants

numpad_path = '/dev/input/event0'
dev = InputDevice(numpad_path)

# 對應的數字鍵盤 keycode
keypad_mapping = {
    69: 'NumLock',
    98: '/',
    55: '*',
    74: '-',
    78: '+',
    14: 'Backspace',
    96: 'Enter',
    82: '0',
    83: '.',
    79: '1',
    80: '2',
    81: '3',
    75: '4',
    76: '5',
    77: '6',
    71: '7',
    72: '8',
    73: '9'
}

num = ""

def keyboard_input_job():
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                keycode = key_event.scancode
                if keycode in keypad_mapping:
                    keyboard_function_job(keypad_mapping[keycode]) 

def keyboard_function_job(key):
    global num

    if key == 'Enter':
        print('pressed Enter')
        is_password_correct()
        num = ""
    elif key == 'Backspace':
        print('pressed Backspace')
        num = num[:-1]
        print("temporary_num:", num)
    elif key == 'NumLock':
        print('pressed NumLock')
        connect_to_smartphone()
    elif key in ['0','1','2','3','4','5','6','7','8','9']:
        num += key
        print("temporary_num:", num)
    else:
        print('pressed other key')

def is_password_correct():
    global num
    ref = db.reference(f'locks/{constants.lock_id}/passwords')
    passwords = ref.get()
    password = passwords.get('password')
    temp_passwords = passwords.get('temp_password')
    if num == password:
        print("password correct")
        # allowed_to_enter()
    else:
        temp_passwords = passwords.get('temp_passwords', {})
        now = int(time.time())
        valid_found = False

        for temp in temp_passwords.values():
            temp_password = temp.get("temp_password")
            start = temp.get("valid_start")
            end = temp.get("valid_until")
            # start_t = datetime.fromtimestamp(start)
            # end_t = datetime.fromtimestamp(end)
            # print(start_t, "~", end_t)

            if temp_password and start and end:
                if num == temp_password and start <= now <= end:
                    valid_found = True
                    break

        if valid_found:
            print("temp_password correct")
            # allowed_to_enter()
        else:
            print("password incorrect or not in valid time range")
            # not_allowed_to_enter()