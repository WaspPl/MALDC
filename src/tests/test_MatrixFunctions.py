import src.scripts.MatrixFunctions as mf
import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
import numpy as np


@pytest.fixture
def mock_Matrix():
    matrix = MagicMock()
    matrix.show.return_value = 1
    return matrix

def test_base64ImageToRGBArray_Base64ImageString_ReturnsArrayOfEGBValues():
    base64 = "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAECAYAAACzzX7wAAAAAXNSR0IArs4c6QAAAC5JREFUGFdjZCAAGMHy29//B9Oeghh8uMD/44IMjE0MYP7/Oob/jJbvwRoIKgAAVWoYBfwtozoAAAAASUVORK5CYII="
    expectedArray = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 183, 239], [0, 183, 239], [0, 0, 0], [0, 0, 0], [0, 183, 239], [0, 183, 239], [0, 0, 0]], [[0, 0, 0], [0, 183, 239], [255, 126, 0], [0, 0, 0], [0, 0, 0], [255, 126, 0], [0, 183, 239], [0, 0, 0]], [[0, 0, 0], [0, 183, 239], [255, 126, 0], [0, 0, 0], [0, 0, 0], [255, 126, 0], [0, 183, 239], [0, 0, 0]]]
    
    result = mf.base64ImageToRGBArray(base64)
    
    assert np.array_equal(result,expectedArray)
    
def test_base64ImageToRGBArray_WrongString_RaisesHTTPError():
    base64 = "Non image string"

    with pytest.raises(HTTPException):
        mf.base64ImageToRGBArray(base64) 
    
def test_isSizeCorrect_ArrayWidthNotDivisibleByMatrixWidth_ReturnsFalse():
    RGBArray = [
                [[],[]],
                [[],[]]
                ]
    
    response = mf.isSizeCorrect(RGBArray,2,3)
    
    assert response == False
    
def test_isSizeCorrect_ArrayWidthEqualToMatrixWidth_ReturnsTrue():
    RGBArray = [
                [[],[]],
                [[],[]]
                ]
    
    response = mf.isSizeCorrect(RGBArray,2,2)
    
    assert response == True
    
def test_isSizeCorrect_ArrayWidthDivisibleByMatrixWidth_ReturnsTrue():
    RGBArray = [
                [[],[],[],[]],
                [[],[],[],[]]
                ]
    
    response = mf.isSizeCorrect(RGBArray,2,2)
    
    assert response == True
    
def test_isSizeCorrect_ArrayHeightGreaterThanMatrixHeight_ReturnsFalse():
    RGBArray = [
                [[],[]],
                [[],[]],
                [[],[]]
                ]
    
    response = mf.isSizeCorrect(RGBArray,2,2)
    
    assert response == False
      
def test_isSizeCorrect_ArrayHeightSmallerThanMatrixHeight_ReturnsFalse():
    RGBArray = [
                [[],[]],
                [[],[]]
                ]
    
    response = mf.isSizeCorrect(RGBArray,2,3)
    
    assert response == False
       
def test_isSizeCorrect_startingLayerPlusSpriteHeightBiggerThanMatrixHeight_ReturnsFalse():
    RGBArray = [
                [[],[]],
                [[],[]]
                ]
    
    response = mf.isSizeCorrect(RGBArray,3,2,2)
    
    assert response == False
    
def test_isSizeCorrect_ArrayHeightEqualToMatrixHeight_ReturnsTrue():
    RGBArray = [
                [[],[]],
                [[],[]]
                ]
    
    response = mf.isSizeCorrect(RGBArray,2,2)
    
    assert response == True
    
def test_divideIntoFrames_oneFrame_returnsASingleFrame():
    
    RGBArray = [
        [[1],[2]],
        [[3],[4]]
    ]
    
    response = mf.divideIntoFrames(RGBArray,2)
    assert np.array_equal(response, [
                                    [[[1],[2]],
                                    [[3],[4]]]
                                    ]
                          )

def test_divideIntoFrames_multipleFrames_returnsAnArrayOfSeparatedFrames():

    
    RGBArray = [
        [[1],[2],[3],[4]],
        [[5],[6],[7],[8]]
    ]
    
    response = mf.divideIntoFrames(RGBArray,2)
    assert np.array_equal(response, [
                                    [[[1],[2]], #frame 1
                                    [[5],[6]]],
                                    [[[3],[4]], #frame 2
                                    [[7],[8]]]
                                    ]
                          )
    
def test_spriteToFlat_2DArray_ReturnsA1DArray():
    frame = [
        [[1, 2, 3], [4, 5, 6]],
        [[7, 8, 9], [10, 11, 12]],
    ]

    result = mf.spriteToFlat(frame)

    expected = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
    ])

    np.testing.assert_array_equal(result, expected)
    
def test_spriteToFlat_2DArrayWithFlipTrue_ReturnsA1DArrayWithEvenRowsFlipped():
    frame = [
        [[1, 2, 3], [4, 5, 6]],
        [[7, 8, 9], [10, 11, 12]],
        [[13, 14, 15], [16, 17, 18]],
        [[19, 20, 21], [22, 23, 24]]
    ]

    result = mf.spriteToFlat(frame, True)

    expected = np.array([
        [1, 2, 3],   [4, 5, 6],
        [10, 11, 12],[7, 8, 9],
        [13, 14, 15],[16, 17, 18],
        [22, 23, 24],[19, 20, 21]
    ])

    np.testing.assert_array_equal(result, expected)
    
def test_displaySprite_RunsShow(mock_Matrix):
    frame = [[[255, 0, 0]]]

    mf.displaySprite(frame, mock_Matrix, startingLayer=0)

    mock_Matrix.show.assert_called_once()
    
def test_displaySprite_WritesPixelsIntoTheMatrix(mock_Matrix):
    frame = [[[255, 0, 0]]]

    mf.displaySprite(frame, mock_Matrix, startingLayer=0)

    # matrix[start:stop] gets translated into matrix.__setitem__(slice(start, stop), flatSprite) so this like extracts those arguments
    sliceUsed, dataWritten = mock_Matrix.__setitem__.call_args[0]
    assert sliceUsed.start == 0
    assert sliceUsed.stop == 1

    assert np.array_equal(
        dataWritten,
        np.array([[255, 0, 0]])
    )
    
def test_displaySprite_HandlesStartingLayerCorrectly(mock_Matrix):
    frame = [[[255, 0, 0]]]

    mf.displaySprite(frame, mock_Matrix, startingLayer=2)

    # matrix[start:stop] gets translated into matrix.__setitem__(slice(start, stop), flatSprite) so this like extracts those arguments
    sliceUsed, dataWritten = mock_Matrix.__setitem__.call_args[0]
    assert sliceUsed.start == 2
    assert sliceUsed.stop == 3

    assert np.array_equal(
        dataWritten,
        np.array([[255, 0, 0]])
    )

