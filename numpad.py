from evdev import InputDevice, ecodes, categorize
from connect import connect_to_smartphone
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
temporary_num = ""

def keyboard_input_job():
    global temporary_num
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                keycode = key_event.scancode
                if keycode in keypad_mapping:
                    print(f'You pressed: {keypad_mapping[keycode]}')
                    keyboard_function_job(keypad_mapping[keycode]) 

def keyboard_function_job(key):
    global temporary_num, num
    print ('keyboard_function_job')

    if key == 'Enter':
        print('pressed Enter')
#         num = temporary_num
#         temporary_num = ""
#         password = "1234"
#         #cardUID, password, start_time, end_time = get_access_settings()
#         if num == password :#and is_now_in_range(start_time, end_time):
#             AllowedToEnter(password)
#         else:
#             NotAllowedToEnter(password)
    elif key == 'NumLock':
        print('pressed NumLock')
        print("lock_id in numpad:", constants.lock_id)
        connect_to_smartphone()
#     elif key is not None:
#         temporary_num += key
#         if len(temporary_num) > 4:
#             temporary_num = temporary_num[1:]
#         lcd.clear()
#         lcd.write_string(temporary_num)