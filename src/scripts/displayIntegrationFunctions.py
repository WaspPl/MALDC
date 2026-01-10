from src.models.DisplayData import DisplayData
from src.scripts.configToObject import Struct
from src.controllers import MatrixController, LCDAndBuzzerController
from asyncio import Queue, wait_for

async def queueManager(settings: Struct, matrix:MatrixController.Matrix, lcd: LCDAndBuzzerController, displayQueue: Queue):
    firstItemInQueue: DisplayData = None
    while True:
        if firstItemInQueue == None: firstItemInQueue = await displayQueue.get() # This will wait for something to be added to the queue
        if matrix.awake == False: await matrix.displayOnAnimation()
        
        await display(firstItemInQueue.message, firstItemInQueue.spriteBase64, firstItemInQueue.spriteReplayTimes)
        
        firstItemInQueue = None
        
        for iteration in range(settings.matrix.random_sprites_before_sleep+1):    
            try:
                firstItemInQueue = await wait_for(displayQueue.get(), timeout=settings.matrix.random_sprite_interval_sec)
                break
            except TimeoutError:
                if iteration == settings.matrix.random_sprites_before_sleep:
                    matrix.displayOffAnimation()
                else:
                    matrix.displayRandomIdleAnimation()

async def display( message: str = "", spriteBase64: str = None, spriteReplayTimes: int = 1):
    
    return