from src.models.DisplayData import DisplayData
from src.scripts.configToObject import Struct
from src.controllers import MatrixController, LCDAndBuzzerController
from asyncio import Queue, wait_for
from typing import List

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

def splitTextToLines(text: str, lineLength: int = 16):
    import string
    import re

    allowedCharacters = (
        string.ascii_letters +  # A-Z, a-z
        string.digits +         # 0-9
        string.punctuation.replace('`', '') +  # remove backtick `
        ' °→←\x7f\n'              # additional known supported characters
    )
    text = ''.join(char for char in text if char in allowedCharacters)
    
    finalArray = []
    sentences = re.split(r'(?<=[.!?])\s+|\n+', text)  # Split by sentence end or new lines
    lineLengths = [lineLength, lineLength - 1]
    line_index = 0
    
    for sentence in sentences:
        words = sentence.split()
        current_line = ""

        for word in words:
            while word:
                line_limit = lineLengths[line_index % 2]
                space_left = line_limit - len(current_line) - (1 if current_line else 0)

                if len(word) <= space_left:
                    current_line += (" " if current_line else "") + word
                    word = ""
                    
                else:
                    if current_line:
                        finalArray.append(current_line)
                        line_index += 1
                        current_line = ""
                    else:
                        finalArray.append(word[:line_limit - 1] + "-")
                        word = word[line_limit - 1:]
                        line_index += 1

        if current_line:
            finalArray.append(current_line)
            line_index += 1

        
    for i in range(len(finalArray)):
        if i % 2 == 1 and i!=len(finalArray)-1:
            while len(finalArray[i]) < lineLength - 1:
                finalArray[i] += " "
            finalArray[i] += "\x00"

    return finalArray
        

async def display( message: str = "", spriteBase64: str = None, spriteReplayTimes: int = 1):
    
    return