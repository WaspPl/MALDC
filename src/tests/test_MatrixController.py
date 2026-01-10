import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import HTTPException
from src.controllers.MatrixController import Matrix

@pytest.mark.asyncio
async def test_displayImage_MultipleFramesRepeatTimesMoreThan1_displaysAllFramesCorrectly():
    obj = Matrix(MagicMock(), "fake")
    fake_frames = [[1],[2]]
    
    with patch("src.scripts.MatrixFunctions.isSizeCorrect", return_value=True), \
        patch("src.scripts.MatrixFunctions.divideIntoFrames", return_value=fake_frames), \
        patch("asyncio.sleep") as sleep_mock, \
        patch("src.scripts.MatrixFunctions.displaySprite") as display_mock:

        await obj.displayImage(
            RGBArray=["RGB"],
            startingLayer=0,
            spriteRepeatTimes=2
        )
    assert display_mock.call_count == 4
    

@pytest.mark.asyncio
async def test_displayImage_MultipleFramesRepeatTimesMoreThan1_WaitBetweenAllTheFramesButNotAfterTheLastOne():
    obj = Matrix(MagicMock(), "fake")
    fake_frames = [[1],[2]]

    with patch("src.scripts.MatrixFunctions.isSizeCorrect", return_value=True), \
        patch("src.scripts.MatrixFunctions.divideIntoFrames", return_value=fake_frames), \
        patch("src.scripts.MatrixFunctions.displaySprite") as display_mock , \
        patch("asyncio.sleep") as sleep_mock:

        await obj.displayImage(
            RGBArray=["RGB"],
            startingLayer=0,
            spriteRepeatTimes=2
        )
    assert sleep_mock.call_count == 3 # 2 frames 2 repeat times so 4 frames total so it should sleep 3 times inbetween
    
@pytest.mark.asyncio
async def test_displayImage_OneFrame_DisplayTheSpriteOnceWithNoWaiting():
    obj = Matrix(MagicMock(), "fake")
    fake_frames = [[1]]

    with patch("src.scripts.MatrixFunctions.isSizeCorrect", return_value=True), \
        patch("src.scripts.MatrixFunctions.divideIntoFrames", return_value=fake_frames), \
        patch("src.scripts.MatrixFunctions.displaySprite") as display_mock, \
        patch("asyncio.sleep") as sleep_mock:

        await obj.displayImage(
            RGBArray=["RGB"],
            startingLayer=0,
            spriteRepeatTimes=1
        )
    assert display_mock.call_count == 1
    assert sleep_mock.call_count == 0 
    
@pytest.mark.asyncio
async def test_getSprites_run_SpritesGetLoadedCorrectly(monkeypatch):
    from PIL import Image
    import numpy as np
    from src.models.Sprites import Sprites
    obj = Matrix(MagicMock(), "neutral")
    fake_imgArray = np.array(Image.new("RGB",(3,2), color=(1,2,3)))
    
    expectedObj = Sprites(
        onOff={
            "on": fake_imgArray,
            "off": fake_imgArray,
        },
        random={
            "common": [fake_imgArray],
            "uncommon": [fake_imgArray],
            "rare": [fake_imgArray],
        },
        rest={
            "neutral": {"eyes": fake_imgArray, "mouth": fake_imgArray},
            "happy": {"eyes": fake_imgArray, "mouth": fake_imgArray},
            "sad": {"eyes": fake_imgArray, "mouth": fake_imgArray},
            "angry": {"eyes": fake_imgArray, "mouth": fake_imgArray},
        },
        speech={
            "a": fake_imgArray,
            "m": fake_imgArray,
            "o": fake_imgArray,
        }
    )

    
    with patch("src.scripts.MatrixFunctions.imageFromPathToRGBArray", return_value=fake_imgArray), \
        patch("os.listdir", return_value=["fake"]):
        result = obj.getSprites()


    assert result.onOff == expectedObj.onOff
    assert result.random == expectedObj.random
    assert result.rest == expectedObj.rest
    assert result.speech == expectedObj.speech
    

@pytest.mark.asyncio
async def test_displayRandomIdleAnimation_spritesExist_callsDisplayImage():
    obj = Matrix(MagicMock(), "neutral")

    fake_sprite = [[[0, 0, 0]]]

    obj.sprites.random = {"common": [fake_sprite]}

    with patch("src.scripts.MatrixFunctions.getRandomIdleAnimationGroup", return_value="common"), \
         patch.object(obj, "displayImage", new_callable=AsyncMock) as mock_display:

        await obj.displayRandomIdleAnimation()

        mock_display.assert_awaited_once_with(fake_sprite)
        
        

@pytest.mark.asyncio
async def test_displayRandomIdleAnimation_noSprites_raisesValueError():
    obj = Matrix(MagicMock(), "neutral")
    
    obj.sprites.random = {"common": []}
    
    with patch("src.scripts.MatrixFunctions.getRandomIdleAnimationGroup", return_value="common"):
        with pytest.raises(ValueError):
            await obj.displayRandomIdleAnimation()