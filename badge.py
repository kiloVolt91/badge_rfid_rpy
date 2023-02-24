#from RPi import GPIO
from pirc522 import RFID
import time, os
from datetime import datetime
from funzioni_badge import *
GPIO.setwarnings(False)
import threading, sys

target_id = [48, 231, 76, 164, 63]

__CARD_MASTER_LIST__ = [
    [140, 223, 184, 157, 118]
]

#HW
red_led_pin = 35
green_led_pin = 37
buzzer = 33
#LCD
lcd_retroill = 40
rs = 11
e = 13
d0 = 7
d1 = 15
d2 = 16
d3 = 32
d4 = 29
d5 = 31 
d6 = 36
d7 = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)


init_pinout(green_led_pin, red_led_pin, buzzer, lcd_retroill)
lcd = init_lcd(rs,e,d0,d1,d2,d3,d4,d5,d6,d7)

print('In attesa di un badge (per chiudere, Ctrl + c): ')
lcd.cursor_pos = (0, 0)
lcd.write_string(u'Attesa Badge')


class Clock:

    def __init__(self, name=None):
        self.stop=False
        self.datetime = None
        self.name = name
     
    def __start_clock(self):
        # Funzione privata
        while self.stop is False:
            self.datetime = datetime.now()
            time.sleep(1)
    
    def start_clock(self):
        # Funzione pubblica
        thr = threading.Thread(target=self.__start_clock)
        thr.start()

    def get_date(self):
        return self.datetime.date().strftime('%d/%m/%Y')

    def get_time(self):
        return self.datetime.strftime('%H:%M:%S')      

    def stop_clock(self):
        self.stop = True



class Rfid:
    
    def __init__(self):
        self.rc522 = RFID()
        self.stop = False
        self.request_error = None
        self.uid_error = None
        self.tag_type = None
        self.uid = None
        self.clock = None
        self.reboot_mode = False
        self.wait_card = False
        self.__set_clock()
        self.wait()
        thr = threading.Thread(target=self.__check_reboot())
        thr.start()
        
    def __check_reboot(self):
        
        while True:
            _restart_ = GPIO.input(12)
            time.sleep(0.1)
            
            if _restart_ == 1 :
                self.reboot_mode = True
                i = 0
                
                for i in range(0,3):
                    lcd.clear()
                    lcd.cursor_pos = (0,0)
                    lcd.write_string("Riavvio fra...")
                    lcd.cursor_pos = (1,0)
                    lcd.write_string(str(3-i)+" secondi")
                    time.sleep(1)
                lcd.clear()
                time.sleep(0.5)
                os.system("echo password | sudo shutdown -r now")
        
    def __set_clock(self):
        self.clock = Clock(name="orologio")                
        self.clock.start_clock()
        thr = threading.Thread(target=self.__write_time)
        thr.start()
        
    def __write_time(self):
        while self.reboot_mode is False:
            if self.clock is not None and self.uid is None and self.wait_card is False:
                lcd.clear()
                lcd.cursor_pos = (0,0)
                lcd.write_string(self.clock.get_date())
                lcd.cursor_pos = (1, 0)
                lcd.write_string(self.clock.get_time())
            time.sleep(1)
        
    def __start_waiting(self):
        self.rc522.wait_for_tag()
        (self.request_error, self.tag_type) = self.rc522.request()
        
        if self.request_error is False:
            self.__set_uid()
        time.sleep(3)
        self.__start_waiting()
        
    def __set_uid(self):
        (self.uid_error, self.uid) = self.rc522.anticoll()
        print("UID", self.uid, type(self.uid))
        if self.uid_error is False:
            self.__process_uid()
    
    def __registra_carta(self):
        import pymysql
        conn = pymysql.connect(host='192.168.x.x',
                             user='user',
                             password='password',
                             db='nome_db')
        cur = conn.cursor()
        query = "INSERT INTO Card(unique_id, active) VALUES('"+\
                ''.join([str(x) for x in self.uid])+"', 0)"
        cur.execute(query)
        conn.commit()
        conn.close()
        lcd.clear()
        
        lcd.cursor_pos = (0,0)
        turn_on(lcd_retroill)
        lcd.write_string("Registrata")
        time.sleep(2)
        turn_off(lcd_retroill)
        self.uid = None
        self.wait_card = False
        
    def __process_uid(self):
        if self.reboot_mode is True:
            return 
        lcd.clear()
        lcd.cursor_pos = (0,0)
        lcd.write_string(self.clock.get_time())
        lcd.cursor_pos = (1,0)
            
        
        if self.wait_card is True:
            self.__registra_carta()
            
        if self.uid in __CARD_MASTER_LIST__:
            
            turn_on(lcd_retroill)
            lcd.write_string("Carta MASTER")
            check_ok(red_led_pin, green_led_pin, buzzer, lcd_retroill)
            self.wait_card = True
            lcd.clear()
            lcd.cursor_pos=(0,0)
            lcd.write_string("Attesa carta..")
            time.sleep(2)
            turn_off(lcd_retroill)
            return
            
        if self.uid == target_id:
            lcd.write_string('Benvenuto')
            check_ok(red_led_pin, green_led_pin, buzzer, lcd_retroill)
        else:
            lcd.write_string('Badge invalido')
            check_no(red_led_pin, green_led_pin, buzzer, lcd_retroill)
        time.sleep(0.1)
        self.uid = None
    
    def wait(self):
        thr = threading.Thread(target=self.__start_waiting)
        thr.start()
                               
    def get_tag_type(self):
        return self.tag_type
    
    def get_uid(self):
        return self.uid
             


             
if __name__ == "__main__":
    
    rfid = Rfid()
    
        
    
    
