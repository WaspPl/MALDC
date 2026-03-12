import asyncio
from email.mime import message
import pytest
import src.scripts.displayIntegrationFunctions as dif
import src.scripts.MatrixFunctions as mf
from pytest import fixture, mark
from unittest.mock import MagicMock, AsyncMock, patch
from src.scripts.settings import load_settings
from src.controllers.LCDAndBuzzerController import LCD
from src.controllers.MatrixController import Matrix
from src.models.Sprites import Sprites 


@pytest.fixture
def mock_GPIO():
    gpio = MagicMock()
    gpio.BCM = "BCM"
    gpio.OUT = "OUT"
    gpio.HIGH = 1
    gpio.LOW = 0
    return gpio

@pytest.fixture
def mock_matrix():
    matrix = MagicMock()
    matrix.emotion = "neutral"
    matrix.sprites = Sprites()
    matrix.displayImage = AsyncMock()
    matrix.displayOnAnimation = AsyncMock()
    matrix.displayOffAnimation = AsyncMock()
    matrix.displayRandomIdleAnimation = AsyncMock()
    matrix.awake = True
    return matrix

@pytest.fixture
def mock_CharLCD():
    charLCD = MagicMock()
    charLCD.create_char = MagicMock(return_value=0)
    charLCD.write_string = MagicMock(return_value=0)
    return charLCD

@pytest.fixture
def mock_lcd(mock_GPIO, mock_CharLCD):
    lcd = LCD(mock_CharLCD, mock_GPIO, load_settings("src/tests/devConfig.yaml"))
    lcd.buzzerPin = 17
    lcd.waitTime = 0.01
    lcd.longWaitTime = 0.01
    lcd.nextScreenWaitTime = 0.01
    lcd.displayLetter = AsyncMock()
    lcd.turnOn = MagicMock()
    lcd.turnOff = MagicMock()
    lcd.setLine = MagicMock()
    lcd.clear = MagicMock()
    return lcd

def test_splitTextToLines_SingleShortLine_DisplaysSingleLinesCorrectly():
    text = "Hello World"
    result = dif.splitTextToLines(text)
    
    assert result == ["Hello World"]

def test_splitTextToLines_LongerLine_SplitsLongerLinesAndAddsTheSpecialCharacterAtTheEndOfEveryOtherLine():
    text = "Lorem Ipsum is simply dummy text"
    result = dif.splitTextToLines(text, lineLength=10)
    
    assert result == ["Lorem", "Ipsum is \x00", "simply", "dummy    \x00", "text"]

def test_splitTextToLines_MultipleSentences_SplitsSentences():
    text = "Hello world. I am a test!"
    result = dif.splitTextToLines(text, lineLength=16)
    
    assert result == ["Hello world.", "I am a test!"]

def test_splitTextToLines_TextWithNewlines_SplitsByNewlines():
    text = "Hello \n world"
    result = dif.splitTextToLines(text)
    
    assert result == ["Hello", "world"]
    
def test_splitTextToLines_TextWithUnsupportedCharacters_UnsupportedCharactersAreFiltereddOutBeforeSplitting():
    text = "Hello🙂 world🚀 I am a test"
    result = dif.splitTextToLines(text)
    
    assert result == ["Hello world I am", "a test"]
    
def test_splitTextToLines_LongWord_HyphenatesTheLongWord():
    text = "Supercalifragilisticexpialidocious"
    result = dif.splitTextToLines(text, lineLength=10)
    
    assert result == [
        "Supercali-",
        "fragilis-\x00",
        "ticexpial-",
        "idocious",
    ]
    
def test_splitTextToLines_TextWithLongWord_HyphenatesTheLongWord():
    text = "Hello Supercalifragilisticexpialidocious world"
    result = dif.splitTextToLines(text, 10)
    
    assert result == [
        "Hello",
        "Supercal-\x00",
        "ifragilis-",
        "ticexpia-\x00",
        "lidocious",
        "world",
    ]
    
def test_splitTextToLines_Text_SpecialCharacterAtTheEndOfEverySecondLineButNotTheLast():
    text = "One two three four five six"
    result = dif.splitTextToLines(text, lineLength=10)

    assert result[1].endswith("\x00")
    assert not result[-1].endswith("\x00")

def test_splitTextToLines_empty_ReturnsEmptyArray():
    text = ""
    result = dif.splitTextToLines(text, lineLength=10)

    assert result == []

def test_splitTextToLines_onlyUnsupported_ReturnsEmptyArray():
    text = "🙂🚀🔥"
    result = dif.splitTextToLines(text, lineLength=10)

    assert result == []

@pytest.mark.parametrize(
    "letter, expected",
    [
        # group "o"
        ("a", "o"),
        ("e", "o"),
        ("i", "o"),
        ("q", "o"),
        ("w", "o"),

        # group "a"
        ("o", "a"),
        ("u", "a"),
        ("l", "a"),
        ("r", "a"),

        # space
        (" ", None),

        # default "m"
        ("b", "m"),
        ("c", "m"),
        ("d", "m"),
        ("f", "m"),
        ("z", "m"),
        ("1", "m"),
        (".", "m"),
    ],
)
def test_matchMouthToLetter(letter, expected):
    assert dif.matchMouthToLetter(letter) == expected
    
def test_matchMouthToLetter_uppercaseLetter_expectedIsSameAsLowercase():
    assert dif.matchMouthToLetter("A") == dif.matchMouthToLetter("a")

@pytest.mark.asyncio
async def test_display_messageNoSprite_displaysMessageOnly(mock_matrix, mock_lcd):
    message = "Hello World"
    
    with patch("src.scripts.displayIntegrationFunctions.asyncio.sleep", new_callable=AsyncMock) as sleep_mock:
        await dif.display(mock_matrix, mock_lcd, message=message)
    
    lettersDisplayed = [call.args[0] for call in mock_lcd.displayLetter.await_args_list]
    assert "".join(lettersDisplayed) == message
    
@pytest.mark.asyncio
async def test_display_messageWithSprite_displaysMessageAndSprite(mock_matrix, mock_lcd):
    message = "Hello World"
    fake_base64 = "fakebase64string"
    with patch("src.scripts.displayIntegrationFunctions.mf.base64ImageToRGBArray", return_value=[[0]*16]*16), \
         patch("src.scripts.displayIntegrationFunctions.asyncio.sleep", new_callable=AsyncMock) as sleep_mock:
        await dif.display(mock_matrix, mock_lcd, message=message, spriteBase64=fake_base64, spriteReplayTimes=2)
   
    lettersDisplayed = [call.args[0] for call in mock_lcd.displayLetter.await_args_list]
    assert "".join(lettersDisplayed) == message

    first_call_args = mock_matrix.displayImage.await_args_list[0][0]
    assert first_call_args[0] == [[0]*16]*16  # RGB array
    assert first_call_args[2] == 2  # spriteReplayTimes