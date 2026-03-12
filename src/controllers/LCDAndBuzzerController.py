import time
import asyncio
from src.scripts.settings import Struct

class LCD:

    def __init__(self, CharLCD, gpio, settings: Struct):
        self.lcd = CharLCD
        self.gpio = gpio
        self.nextIndicator = self.lcd.create_char(0,(0b00000,0b00100,0b00100,0b00100,0b00100,0b11111,0b01110,0b00100,))
        self.buzzerPin = settings.buzzer.pin
        self.longWaitList = settings.lcd.long_wait_list
        self.waitTime = settings.lcd.wait_time
        self.longWaitTime = settings.lcd.long_wait_time
        self.nextScreenWaitTime = settings.lcd.next_screen_wait_time
        self.lineLength = settings.lcd.line_length
        self.lineCount = settings.lcd.line_count
        
        gpio.setmode(gpio.BCM)
        gpio.setup(self.buzzerPin, gpio.OUT)
        gpio.output(self.buzzerPin, gpio.HIGH) 
        
    async def beep(self):
        self.gpio.output(self.buzzerPin, self.gpio.LOW)  # Turn ON buzzer
        await asyncio.sleep(0.01)  
        self.gpio.output(self.buzzerPin, self.gpio.HIGH)   # Turn OFF buzzer
        
        
    async def displayLetter(self,letter):
        self.lcd.write_string(letter)
        if letter == " ":
            await asyncio.sleep(self.waitTime)   
        elif letter in self.longWaitList:
            await asyncio.sleep(self.longWaitTime)
        else:
            await self.beep()
            await asyncio.sleep(self.waitTime)
        
    def turnOff(self):
        self.lcd.clear()
        self.lcd.backlight_enabled = False
        
    def turnOn(self):
        self.lcd.backlight_enabled = True
        
    def clear(self):
        self.lcd.clear()
        
    def setLine(self,line):
        self.lcd.cursor_pos = (line, 0)
        