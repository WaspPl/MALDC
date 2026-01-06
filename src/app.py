from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from asyncio import create_task, Queue, wait_for, TimeoutError
from src.models.DisplayData import DisplayData
from src.scripts import configToObject
from src.controllers import MatrixController, LCDAndBuzzerController


displayQueue: Queue = Queue()

async def queueManager(settings, matrix, lcd):
    itemToBeDisplayed: DisplayData = None
    while True:
        if itemToBeDisplayed == None: itemToBeDisplayed = await displayQueue.get() # This will wait for something to be added to the queue
        
        # await display itemToBeDisplayed
        print(f'Display data: {itemToBeDisplayed}')
        
        itemToBeDisplayed = None
        
        for spritesPlayed in range(settings.matrix.random_sprites_before_sleep+1):
            if itemToBeDisplayed == None: itemToBeDisplayed = await wait_for(displayQueue.get())
            
            if matrix.awake == False: print("wake up")
            
            print(f"display {itemToBeDisplayed.message} with sprite {itemToBeDisplayed.spriteBase64} played times: {itemToBeDisplayed.spriteReplayTimes}")
            
            try:
                itemToBeDisplayed = await wait_for(displayQueue.get(), timeout=settings.matrix.random_sprite_interval_sec)
                break
            except TimeoutError:
                if spritesPlayed == settings.matrix.random_sprites_before_sleep:
                    #await matrix turn off
                    print("sleep")
                else:
                    #await matrix random
                    print(f"random {spritesPlayed}/{settings.matrix.random_sprites_before_sleep}")


@asynccontextmanager
async def queueLifespan(app: FastAPI):
    import neopixel
    import board
    import CharLCD
    
    settings = configToObject.settings
    
    numberOfLEDs = settings.matrix.rows * settings.matrix.columns
    
    #set up the controllers
    matrixController = MatrixController.Matrix(neopixel.NeoPixel(pin=board.D18,n=numberOfLEDs, auto_write=False, pixel_order=neopixel.GRB, brightness=settings.matrix.brightness))
    lCDAndBuzzerController = LCDAndBuzzerController.LCD(CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=settings.lcd.columns, rows=settings.lcd.row, backlight_enabled=settings.backlight_enabled_by_default))
    
    task = create_task(queueManager(configToObject.settings, matrixController, lCDAndBuzzerController)) # As long as queueManager runs the API will be alive
    yield
    task.cancel()


app: FastAPI = FastAPI(lifespan=queueLifespan)

@app.post("/display")
async def displayText(data: DisplayData):
    await displayQueue.put(data)
    return Response(status_code=202)