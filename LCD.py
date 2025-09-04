from time import sleep
from RPLCD.i2c import CharLCD

lcd = None

def setup_lcd():
    global lcd
    lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
    lcd.clear()

def destroy_lcd():
    global lcd
    lcd.clear()
    lcd.backlight_enabled = False
    lcd.close()  

def LCD_display_job(line1 = "", cursor_pos1=(0,0), line2 = "", cursor_pos2=(1,7), need_clear = True):
    global lcd
    lcd.clear()
    lcd.cursor_pos = cursor_pos1
    lcd.write_string(line1)
    lcd.cursor_pos = cursor_pos2
    lcd.write_string(line2)
    if need_clear: 
        sleep(2)
        lcd.clear()

def clear_lcd_and_show_prompt():
    global lcd
    lcd.clear()
    LCD_display_job(line1="tap card or", line2="input password", cursor_pos2=(1,1), need_clear=False)    
