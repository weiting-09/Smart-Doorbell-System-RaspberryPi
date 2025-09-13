from LCD import LCD_display_job
from LED import turn_on_green_led, turn_off_green_led, turn_on_red_led, turn_off_red_led
import time
from firebase_admin import db
import constants
from lock import lock_the_door, unlock_the_door


def allowed_to_enter(method="unknown"):
    if(is_security_mode()): 
        print("security_mode: cannot open the door")
        LCD_display_job(line1="security_mode:", line2="Keep closed", cursor_pos2=(1,4), display_time=2)
        return
    turn_on_green_led()
    unlock_the_door()
    LCD_display_job(line1="Welcome!", display_time=2)
    turn_off_green_led()
    lock_the_door()
    if method != "APP": set_unlock_logs(method=method, status="successed")


def not_allowed_to_enter(method="unknown"):
    turn_on_red_led()
    LCD_display_job(line1="not allow", line2="to enter", display_time=2)
    turn_off_red_led()
    set_unlock_logs(method=method, status="failed")

def is_security_mode():
    ref = db.reference(f'locks/{constants.lock_id}/security_mode')
    if(ref.get()): 
        print("security_mode is true")
        return True
    else: 
        print("security_mode is false")
        return False

def set_unlock_logs(method, status, timestamp=None, user="unknown"):
    if timestamp is None:
        timestamp = int(time.time())
    ref = db.reference(f'locks/{constants.lock_id}/unlock_logs')
    ref.push({
        'method': method,
        'status': status,
        'time': timestamp,
        'user': user
    })
