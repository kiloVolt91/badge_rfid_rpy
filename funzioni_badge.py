from RPi import GPIO
import time
from RPLCD import CharLCD
# 
# rs = 11
# e = 13
# d1 = 29
# d2 = 31 
# d3 = 36
# d4 = 37


def init_pinout(red_ledPin, green_ledPin, buzzerPin,lcd_retroill):
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setwarnings(False)
    
    GPIO.setup(red_ledPin, GPIO.OUT)
    GPIO.setup(green_ledPin, GPIO.OUT)
    GPIO.setup(buzzerPin, GPIO.OUT)
    GPIO.setup(lcd_retroill, GPIO.OUT)
    
    GPIO.output(red_ledPin, GPIO.LOW)
    GPIO.output(green_ledPin, GPIO.LOW)
    GPIO.output(buzzerPin, GPIO.LOW)
    GPIO.output(lcd_retroill, GPIO.LOW)
    #possibile realizzare vettore con gli output
    return (red_ledPin, green_ledPin, buzzerPin,lcd_retroill)


def init_lcd(rs,e,d0,d1,d2,d3,d4,d5,d6,d7):
    lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=rs, pin_e=e, pins_data=[d0,d1, d2, d3, d4, d5, d6, d7])
    return (lcd)
    
def turn_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    return

def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)
    return

def buzzer_negative_check(pin):
    t=0.1
    turn_on(pin)
    time.sleep(t)
    turn_off(pin)
    time.sleep(t)
    turn_on(pin)
    time.sleep(t)
    turn_off(pin)
    time.sleep(t)
    turn_on(pin)
    time.sleep(t)
    turn_off(pin)
    time.sleep(1)
    return

def buzzer_positive_check(pin):
    turn_on(pin)
    time.sleep(1)
    turn_off(pin)
    return

def check_ok(red_led_pin, green_led_pin, buzzer, lcd_retroill):
            turn_on(lcd_retroill)
            turn_on(red_led_pin)
            turn_off(green_led_pin)
            buzzer_positive_check(buzzer)
            turn_off(red_led_pin)
            time.sleep(2)
            turn_off(lcd_retroill)
            return
        
def check_no(red_led_pin, green_led_pin, buzzer, lcd_retroill):
             turn_on(lcd_retroill)
             turn_on(green_led_pin)
             turn_off(red_led_pin)
             buzzer_negative_check(buzzer)
             turn_off(green_led_pin)
             turn_off(buzzer)
             time.sleep(2)
             turn_off(lcd_retroill)
             return

    

    