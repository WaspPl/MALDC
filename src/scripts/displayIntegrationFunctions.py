from src.models.DisplayData import DisplayData
from src.scripts.configToObject import Struct
from src.controllers import MatrixController, LCDAndBuzzerController
from asyncio import Queue, wait_for
from typing import List
import asyncio
import src.scripts.MatrixFunctions as mf
import src.scripts.displayIntegrationFunctions as dif


async def queueManager(settings: Struct, matrix:MatrixController.Matrix, lcd: LCDAndBuzzerController, displayQueue: Queue):
    firstItemInQueue: DisplayData = None
    while True:
        if firstItemInQueue == None: firstItemInQueue = await displayQueue.get() # This will wait for something to be added to the queue
        if matrix.awake == False: await matrix.displayOnAnimation()
        
        await display(matrix, lcd, firstItemInQueue.message, firstItemInQueue.spriteBase64, firstItemInQueue.spriteReplayTimes)
        
        firstItemInQueue = None
        
        for iteration in range(settings.matrix.random_sprites_before_sleep+1):    
            try:
                firstItemInQueue = await wait_for(displayQueue.get(), timeout=settings.matrix.random_sprite_interval_sec)
                break
            except TimeoutError:
                if iteration == settings.matrix.random_sprites_before_sleep:
                    await matrix.displayOffAnimation()
                else:
                    await matrix.displayRandomIdleAnimation()

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

async def display( matrix: MatrixController.Matrix, lcd : LCDAndBuzzerController.LCD, message: str = "", spriteBase64: str = None, spriteReplayTimes: int = 1):
    lines = dif.splitTextToLines(message, lcd.lineLength)
    
    if spriteBase64:
        animationRGBArray = mf.base64ImageToRGBArray(spriteBase64)
        animation = asyncio.create_task(matrix.displayImage(animationRGBArray, 0, spriteReplayTimes))
    else:
        animation = asyncio.create_task(asyncio.sleep(0))
    
    lcd.turnOn()
    
    for lineIndex, line in enumerate(lines):
        if animation.done(): await matrix.displayImage(matrix.sprites.rest[matrix.emotion]["eyes"], 0)
        
        lcd.setLine((lineIndex) % 2)
        
        for letter in line:
            await lcd.displayLetter(letter)
            if animation.done():
                mouth = matchMouthToLetter(letter)
                if not mouth:
                    await matrix.displayImage(matrix.sprites.rest[matrix.emotion]["mouth"], 4)
                else:
                    await matrix.displayImage(matrix.sprites.speech[mouth], 4)
        
        
        if animation.done(): await matrix.displayImage(matrix.sprites.rest[matrix.emotion]["mouth"], 4)
        
        if lineIndex%2==1 and lineIndex!=len(lines)-1:
            await asyncio.sleep(lcd.nextScreenWaitTime)
            lcd.clear()
        
    if animation and not animation.done(): await animation
    
    await matrix.displayImage(matrix.sprites.rest[matrix.emotion]["eyes"], 0)
    await matrix.displayImage(matrix.sprites.rest[matrix.emotion]["mouth"], 4)
    
    await asyncio.sleep(3)
    
    lcd.turnOff()
    
    return

def matchMouthToLetter(letter: str):
    letter = letter.lower()
    if letter in {"a","e","i","q","w"}: return "o"
    if letter in {"o", "u", "l", "r"}: return "a"
    if letter == " ": return None
    return "m"