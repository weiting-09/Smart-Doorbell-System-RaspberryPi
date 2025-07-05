from time import time, sleep
import sys, smbus
import requests
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD
import threading
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

sys.modules['smbus'] = smbus

# 初始化 Firebase
cred = credentials.Certificate("MY_CREDENTIAL_FILE.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://MY_DATABASE_URL/'
})

GPIO.setmode(GPIO.BCM)
LED_green = 21
LED_red = 20
button = 26
Buzzer = 19
IR_PIN = 16
num = ""
temporary_num = ""

KEYS = {
    0xff6897: '0',
    0xff30cf: '1',
    0xff18e7: '2',
    0xff7a85: '3',
    0xff10ef: '4',
    0xff38c7: '5',
    0xff5aa5: '6',
    0xff42bd: '7',
    0xff4ab5: '8',
    0xff52ad: '9',
    0xff906f: 'EQ'
}

GPIO.setup(LED_green, GPIO.OUT)
GPIO.setup(LED_red, GPIO.OUT)
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
lcd.clear()
reader = SimpleMFRC522()

CL = [0, 131, 147, 165, 175, 196, 220, 247]
CM = [0, 262, 294, 330, 349, 392, 440, 494]
CH = [0, 523, 587, 659, 698, 784, 880, 988]

melody_doorBell = [CH[3], CH[1]]
beat_doorBell = [1, 2]
Buzz = GPIO.PWM(Buzzer, 440)

def get_access_settings():
    data = db.reference('access_control').get()
    return (
        int(data.get("cardUID", 0)),
        data.get("password", ""),
        data.get("allow_start_time", ""),
        data.get("allow_end_time", "")
    )

def update_lock_status(opened: bool):
    db.reference('lock_status').set({'opened': opened})

def log_access(status, method):
    db.reference('access_log').push({
        'status': status,
        'method': method,
        'timestamp': str(datetime.now())
    })

def myCallback(channel):
    Buzz.start(50)
    for i in range(len(melody_doorBell)):
        Buzz.ChangeFrequency(melody_doorBell[i])
        sleep(beat_doorBell[i] * 0.5)
    Buzz.stop()

GPIO.add_event_detect(button, GPIO.FALLING, callback=myCallback, bouncetime=350)

def binary_aquire(pin, duration):
    t0 = time()
    results = []
    while (time() - t0) < duration:
        results.append(GPIO.input(pin))
    return results

def on_ir_receive(pinNo, bouncetime=150):
    data = binary_aquire(pinNo, bouncetime / 1000.0)
    if len(data) < bouncetime:
        return
    rate = len(data) / (bouncetime / 1000.0)
    pulses = []
    i_break = 0
    for i in range(1, len(data)):
        if data[i] != data[i-1] or i == len(data)-1:
            pulses.append((data[i-1], int((i-i_break)/rate*1e6)))
            i_break = i
    outbin = ""
    for val, us in pulses:
        if val != 1:
            continue
        if outbin and us > 2000:
            break
        elif us < 1000:
            outbin += "0"
        elif 1000 < us < 2000:
            outbin += "1"
    try:
        return int(outbin, 2)
    except ValueError:
        return None

def AllowedToEnter(method="unknown"):
    GPIO.output(LED_green, GPIO.HIGH)
    lcd.clear()
    lcd.write_string("Welcome")
    sleep(1)
    GPIO.output(LED_green, GPIO.LOW)
    lcd.clear()
    update_lock_status(True)
    log_access("allowed", method)

def NotAllowedToEnter(method="unknown"):
    GPIO.output(LED_red, GPIO.HIGH)
    lcd.clear()
    lcd.write_string("not allowed")
    lcd.cursor_pos = (1, 7)
    lcd.write_string("to enter")
    sleep(1)
    GPIO.output(LED_red, GPIO.LOW)
    lcd.clear()
    update_lock_status(False)
    log_access("denied", method)

def is_now_in_range(start_str, end_str):
    now = datetime.now()
    start = datetime.strptime(start_str, "%Y/%m/%d %H:%M")
    end = datetime.strptime(end_str, "%Y/%m/%d %H:%M")
    return start <= now <= end

def IR_job():
    global temporary_num, num
    while True:
        GPIO.wait_for_edge(IR_PIN, GPIO.FALLING)
        sleep(0.02)
        code = on_ir_receive(IR_PIN)
        if code is None:
            continue
        key = KEYS.get(code, None)
        if key == 'EQ':
            num = temporary_num
            temporary_num = ""
            cardUID, password, start_time, end_time = get_access_settings()
            if num == password and is_now_in_range(start_time, end_time):
                AllowedToEnter("password")
            else:
                NotAllowedToEnter("password")
        elif key is not None:
            temporary_num += key
            if len(temporary_num) > 4:
                temporary_num = temporary_num[1:]
            lcd.clear()
            lcd.write_string(temporary_num)

def RFID_job():
    while True:
        id, text = reader.read()
        cardUID, password, start_time, end_time = get_access_settings()
        if id == cardUID and is_now_in_range(start_time, end_time):
            AllowedToEnter("RFID")
        else:
            NotAllowedToEnter("RFID")
        sleep(1)
        lcd.clear()

def destroy():
    Buzz.stop()
    GPIO.output(Buzzer, 1)
    GPIO.cleanup()
    lcd.clear()

def main():
    try:
        lcd.clear()
        lcd.write_string("Enter password")
        lcd.cursor_pos = (1, 5)
        lcd.write_string("or tap card")
        threading.Thread(target=IR_job).start()
        threading.Thread(target=RFID_job).start()
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Exit by Ctrl+C")
    finally:
        destroy()

if __name__ == "__main__":
    main()
