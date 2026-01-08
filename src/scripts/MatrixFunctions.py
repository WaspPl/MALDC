
import numpy as np
from typing import List

def base64ImageToRGBArray(base64String: str):
    from PIL import Image, UnidentifiedImageError
    from base64 import b64decode
    from io import BytesIO
    from fastapi import HTTPException
    
    try:
        imageBytes = b64decode(base64String)
        image = Image.open(BytesIO(imageBytes)).convert("RGB")
    except (UnidentifiedImageError, ValueError):
        raise HTTPException(status_code=400, detail="Sprite couldn't be resolved. Please provide correct Byte64 string")
    return np.array(image)


def isSizeCorrect(Array: List[List[List[int]]], matrixHeight: int, matrixWidth: int, startingLayer: int = 0):
    
    RGBArray = np.array(Array)
    arrayHeight = RGBArray.shape[0]
    arrayWidth = RGBArray.shape[1]
    
    if arrayWidth % matrixWidth != 0: return False # The sprite/spritesheet must have all the frames complete
    if arrayHeight + startingLayer > matrixHeight: return False # The sprite sheet is horisontal, so it cant be bigger than the matrix itself
    return True

def divideIntoFrames(Array: List[List[List[int]]], matrixWidth:int):
    RGBArray = np.array(Array)    
    result = []
    
    for columnNumber in range(0,RGBArray.shape[1],matrixWidth): # from 0 to the end of the RGB Array with steps of matrix width
        frame = RGBArray[:, columnNumber:columnNumber + matrixWidth,:]
        result.append(frame)
    
    return result

def displaySprite(frame: List[List[List[int]]], matrix, startingLayer: int = 0, flip: bool = False):
    sprite = np.array(frame)
    startingLayerOffset = startingLayer*sprite.shape[1]
    
    flatSprite = spriteToFlat(sprite, flip)
    matrix[startingLayerOffset:startingLayerOffset+flatSprite.shape[0]] = flatSprite # from the offset to the end replace the matrix values with sprite's rgb pixels
    matrix.show()
    
def spriteToFlat(frame:List[List[List[int]]], flip=False):
    sprite = np.array(frame)
    if flip:
        sprite = np.array([row[::-1] if i % 2 == 1 else row for i,  row in enumerate(sprite)])
 
    flatSprite = sprite.reshape(-1,3)
    return flatSprite
    
    