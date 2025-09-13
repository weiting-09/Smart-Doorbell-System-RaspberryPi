from datetime import datetime
import time
from LCD import LCD_display_job, clear_lcd_and_show_prompt
from access_control import allowed_to_enter, not_allowed_to_enter
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
        clear_lcd_and_show_prompt()
    elif key == 'Backspace':
        print('pressed Backspace')
        num = num[:-1]
        LCD_display_job(line1="Enter password:", line2=num,
                        cursor_pos2=(1, 0))
        print("num:", num)
    elif key == 'NumLock':
        print('pressed NumLock')
        connect_to_smartphone()
    elif key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        num += key
        LCD_display_job(line1="Enter password:", line2=num,
                        cursor_pos2=(1, 0))
        print("num:", num)
    # 僅開發時使用
    elif key == '+':
        print('pressed +')
        db.reference(f'locks/{constants.lock_id}/RFIDs/add_new_RFID').set(True)
    elif key == '-':
        print('pressed -')
        db.reference(
            f'locks/{constants.lock_id}/RFIDs/add_new_RFID').set(False)
    # 僅開發時使用
    else:
        print('pressed other key')


def is_password_correct():
    global num
    try:
        ref = db.reference(f'locks/{constants.lock_id}/passwords')
        passwords = ref.get()
        if passwords is None:
            print("No passwords set in database.")
            LCD_display_job(line1="Please setup", line2="on phone first",
                            cursor_pos2=(1, 2))
            return
        password = passwords.get('password')
        if num == password:
            print("password correct")
            allowed_to_enter(method="password")
            return
        else:
            temp_passwords = passwords.get('temp_passwords', {})
            now = int(time.time())
            valid_found = False

            if temp_passwords is None:
                print("No temporary passwords set in database.")
                LCD_display_job(line1="Please setup", line2="on phone first",
                                cursor_pos2=(1, 2))
                return
            else:
                for temp in temp_passwords.values():
                    temp_password = temp.get("temp_password")
                    start = temp.get("valid_start")
                    end = temp.get("valid_until")

                    if temp_password and start and end:
                        if num == temp_password and start <= now <= end:
                            valid_found = True
                            break

            if valid_found:
                print("temp_password correct")
                allowed_to_enter(method="temporary password")
            else:
                print("password incorrect or not in valid time range")
                not_allowed_to_enter(method="password")
    except Exception as e:
        print(f"Error checking password: {e}")
