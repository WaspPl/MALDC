from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from asyncio import create_task, Queue, wait_for, TimeoutError
from src.models.DisplayData import DisplayData
from src.scripts import configToObject

displayQueue: Queue = Queue()

async def queueManager(settings, hardwareController):
    itemToBeDisplayed: DisplayData = None
    while True:
        if itemToBeDisplayed == None: itemToBeDisplayed = await displayQueue.get() # This will wait for something to be added to the queue
        
        # await display itemToBeDisplayed
        print(f'Display data: {itemToBeDisplayed}')
        
        itemToBeDisplayed = None
        
        for spritesPlayed in range(settings.matrix.random_sprites_before_sleep+1):
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
    hardwareController = ""
    task = create_task(queueManager(configToObject.settings, hardwareController)) # As long as queueManager runs the API will be alive
    yield
    task.cancel()


app: FastAPI = FastAPI(lifespan=queueLifespan)

@app.post("/display")
async def displayText(data: DisplayData):
    await displayQueue.put(data)
    return Response(status_code=202)