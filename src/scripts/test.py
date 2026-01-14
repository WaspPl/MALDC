from RPLCD.i2c import CharLCD
from time import sleep
from src.controllers import MatrixController, LCDAndBuzzerController
import neopixel
import board
import RPi.GPIO as GPIO
from src.scripts.configToObject import loadSettings
import src.scripts.displayIntegrationFunctions as dif

# lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, backlight_enabled=True)
# lcd.write_string('Hello World!')
# sleep(5)
# lcd.clear()
settings = loadSettings("config.yaml")

matrixController = MatrixController.Matrix(neopixel.NeoPixel(pin=board.D18,n=64, auto_write=False, pixel_order=neopixel.GRB, brightness=0.2), "neutral", settings)
lCDAndBuzzerController = LCDAndBuzzerController.LCD(CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, backlight_enabled=True), GPIO, settings)

async def test():
    print(dif.splitTextToLines("This is a test message to check the splitting of text into multiple lines and see how it handles longer texts that exceed the line length."))
    await dif.display(matrixController, lCDAndBuzzerController, "This is a test message to check the splitting of text into multiple lines and see how it handles longer texts that exceed the line length.", None, 0)
import asyncio
asyncio.run(test())
