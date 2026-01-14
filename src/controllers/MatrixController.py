from src.scripts.configToObject import Struct
import src.scripts.MatrixFunctions as mf
from fastapi import HTTPException
import asyncio
from typing import List
from src.models.Sprites import Sprites
from PIL import Image
from pathlib import Path
import numpy as np
import os

class Matrix :
    def __init__(self, neoPixel, emotion: str, settings: Struct):
        self.matrix = neoPixel
        self.emotion= emotion
        self.animationInProgress = False
        self.awake = False
        self.matrixHeight = settings.matrix.rows
        self.matrixWidth = settings.matrix.columns
        self.flipEveryOtherRow = settings.matrix.flip_every_other_row
        self.spritesFolder = settings.matrix.sprites_folder
        self.sprites = self.getSprites()
        self.randomIdleAnimationWeights = settings.matrix.random_sprites_weights
        

    
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

    def getSprites(self):
        spr = Sprites()
        
        # set on and off animations
        spr.onOff["on"] = mf.imageFromPathToRGBArray(Path(self.spritesFolder,"onOff/on.png"))
        spr.onOff["off"] = mf.imageFromPathToRGBArray(Path(self.spritesFolder,"onOff/off.png"))
        
        # set random animations
        
        rarities = ["common", "uncommon", "rare"]
        for rarity in rarities:
            files = os.listdir(Path(self.spritesFolder,"random", rarity))
            for file in files:
                spr.random[rarity].append(mf.imageFromPathToRGBArray(Path(self.spritesFolder, "random", rarity, file)))
        
        # set rest animations
        moods = ["neutral", "happy", "sad", "angry"]
        for mood in moods:
            spr.rest[mood]["eyes"] = mf.imageFromPathToRGBArray(Path(self.spritesFolder, "rest", mood, "eyes.png"))
            spr.rest[mood]["mouth"] = mf.imageFromPathToRGBArray(Path(self.spritesFolder, "rest", mood, "mouth.png"))
        
        # set speech animations
        mouthShapes = ["a", "m", "o"]
        for shape in mouthShapes:
            spr.speech[shape] = mf.imageFromPathToRGBArray(Path(self.spritesFolder, "speech", f"{shape}.png"))
        
        return spr
    
    async def displayRandomIdleAnimation(self):
        import random
        group = mf.getRandomIdleAnimationGroup(self.randomIdleAnimationWeights.common, self.randomIdleAnimationWeights.uncommon, self.randomIdleAnimationWeights.rare)
        
        spriteList = self.sprites.random.get(group)
        
        if not spriteList:
            raise ValueError("No idle sprites for group %s", group)
        
        randomSprite = random.choice(spriteList)
        

        await self.displayImage(randomSprite)
        return 
    
    async def displayOnAnimation(self):
        self.awake = True
        await self.displayImage(self.sprites.onOff["on"])

    async def displayOffAnimation(self):
        self.awake = False
        await self.displayImage(self.sprites.onOff["off"])
