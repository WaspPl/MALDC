from fastapi import FastAPI
from contextlib import asynccontextmanager
from asyncio import create_task, Queue, wait_for, TimeoutError
from models import DisplayData

displayQueue: Queue = Queue()

async def queueManager():
    itemToBeDisplayed: DisplayData = None
    while True:
        if itemToBeDisplayed == None: itemToBeDisplayed = await displayQueue.get() # This will wait for something to be added to the queue
        
        # await display itemToBeDisplayed
        print(f'Display data: {itemToBeDisplayed}')
        
        itemToBeDisplayed = None
        
        for timePassed in range(30): # replace this with a yaml setting
            try:
                itemToBeDisplayed = await wait_for(displayQueue.get(), timeout=5) # replace with yaml
                break
            except TimeoutError:
                if timePassed == 30:
                    #await matrix turn off
                    print("sleep")
                else:
                    #await matrix random
                    print("random")

@asynccontextmanager
async def queueLifespan(app: FastAPI):
    create_task(queueManager()) # As long as queueManager runs the API will be alive
    yield


app: FastAPI = FastAPI(lifespan=queueLifespan)