from src.scripts import configToObject
import src.scripts.MatrixFunctions as mf
from fastapi import HTTPException
import asyncio
from typing import List
class Matrix :
    
    def __init__(self, neoPixel, emotion):
        self.matrix = neoPixel
        self.emotion: str = emotion
        self.animationInProgress = False
        self.awake = False
        self.matrixHeight = configToObject.settings.matrix.rows
        self.matrixWidth = configToObject.settings.matrix.columns
        self.flipEveryOtherRow = configToObject.settings.matrix.flip_every_other_row

    
    async def displayImage(self, RGBArray: List[List[List[int]]], startingLayer: int = 0, spriteRepeatTimes:int =1):
        if mf.isSizeCorrect(RGBArray,self.matrixHeight,self.matrixWidth,startingLayer) == False: 
            raise HTTPException(status_code=400, detail="Sprite size does not match matrix dimensions")
        
        frameArray = mf.divideIntoFrames(RGBArray,self.matrixWidth)
        
        for repeat in range(spriteRepeatTimes):
            for frameNumber, frame in enumerate(frameArray):
                mf.displaySprite(frame, self.matrix, startingLayer, self.flipEveryOtherRow)
                if not (repeat == spriteRepeatTimes-1 and frameNumber == len(frameArray)-1):
                    await asyncio.sleep(0.1)
        return

        