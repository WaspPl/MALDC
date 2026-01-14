from fastapi import FastAPI, Response, HTTPException
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
    from RPLCD.i2c import CharLCD
    import RPi.GPIO as GPIO
    
    settings = configToObject.loadSettings("config.yaml")
    
    numberOfLEDs = settings.matrix.rows * settings.matrix.columns
    
    #set up the controllers
    matrixController = MatrixController.Matrix(neopixel.NeoPixel(pin=board.D18,n=numberOfLEDs, auto_write=False, pixel_order=neopixel.GRB, brightness=settings.matrix.brightness), "neutral", settings)
    lCDAndBuzzerController = LCDAndBuzzerController.LCD(CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=settings.lcd.line_length, rows=settings.lcd.line_count, backlight_enabled=settings.lcd.backlight_enabled_by_default), GPIO, settings)
    
    task = create_task(queueManager(settings, matrixController, lCDAndBuzzerController, displayQueue)) # As long as queueManager runs the API will be alive
    yield
    task.cancel()


app: FastAPI = FastAPI(lifespan=queueLifespan)

@app.post("/display", status_code=202)
async def displayText(data: DisplayData):
    if data.message is None and data.spriteBase64 is None:
        raise HTTPException(status_code=400, detail="At least one of those fields must me specified: message, spriteBase64")
    await displayQueue.put(data)