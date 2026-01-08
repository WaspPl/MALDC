import pytest
from unittest.mock import MagicMock, patch
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