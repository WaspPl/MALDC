from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from asyncio import create_task, Queue, wait_for, TimeoutError
from src.models.DisplayData import DisplayData
from src.scripts import configToObject
from src.controllers import MatrixController, LCDAndBuzzerController
from src.scripts.displayIntegrationFunctions import queueManager


displayQueue: Queue = Queue()


@asynccontextmanager
async def queueLifespan(app: FastAPI):
    import neopixel
    import board
    import CharLCD
    import RPi.GPIO as GPIO
    
    settings = configToObject.settings
    
    numberOfLEDs = settings.matrix.rows * settings.matrix.columns
    
    #set up the controllers
    matrixController = MatrixController.Matrix(neopixel.NeoPixel(pin=board.D18,n=numberOfLEDs, auto_write=False, pixel_order=neopixel.GRB, brightness=settings.matrix.brightness), "neutral", settings)
    lCDAndBuzzerController = LCDAndBuzzerController.LCD(CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=settings.lcd.columns, rows=settings.lcd.row, backlight_enabled=settings.backlight_enabled_by_default), GPIO, settings)
    
    task = create_task(queueManager(configToObject.settings, matrixController, lCDAndBuzzerController)) # As long as queueManager runs the API will be alive
    yield
    task.cancel()


app: FastAPI = FastAPI(lifespan=queueLifespan)

@app.post("/display")
async def displayText(data: DisplayData):
    await displayQueue.put(data)
    return Response(status_code=202)