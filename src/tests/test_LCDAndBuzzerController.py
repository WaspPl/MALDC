import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock, patch, call
from src.scripts.configToObject import loadSettings
from src.controllers.LCDAndBuzzerController import LCD

@pytest.fixture
def mock_GPIO():
    gpio = MagicMock()
    gpio.BCM = "BCM"
    gpio.OUT = "OUT"
    gpio.HIGH = 1
    gpio.LOW = 0
    return gpio

@pytest.fixture
def mock_CharLCD():
    charLCD = MagicMock()
    charLCD.create_char = MagicMock(return_value=0)
    charLCD.write_string = MagicMock(return_value=0)
    return charLCD

@pytest.fixture
def mock_lcd(mock_GPIO, mock_CharLCD):
    lcd = LCD(mock_CharLCD, mock_GPIO, loadSettings("src/tests/devConfig.yaml"))
    lcd.buzzerPin = 17
    lcd.waitTime = 0.1
    lcd.longWaitTime = 0.5
    return lcd

@pytest.mark.asyncio
async def test_beep_GPIOgoesOnAndThenOff(mock_lcd, mock_GPIO):
    await mock_lcd.beep()

    calls = mock_GPIO.output.call_args_list
    # Starts with a 1, because the 0th call is the setup
    assert calls[1] == call(mock_lcd.buzzerPin, mock_GPIO.LOW)
    assert calls[2] == call(mock_lcd.buzzerPin, mock_GPIO.HIGH)

@pytest.mark.asyncio
async def test_displayLetter_oneLetter_writesTheLetterOnce(mock_lcd, mock_CharLCD):
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock):
        await mock_lcd.displayLetter("x")
    mock_CharLCD.write_string.assert_called_once_with("x")

@pytest.mark.asyncio
async def test_displayLetter_space_waitsNormalTimeAndDoesntBeep(mock_lcd):
    mock_lcd.beep = MagicMock()
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock) as mockSleep:
        await mock_lcd.displayLetter(" ")
    mockSleep.assert_awaited_once_with(mock_lcd.waitTime)
    mock_lcd.beep.assert_not_called()

@pytest.mark.asyncio
async def test_displayLetter_letter_waitsNormalTimeAndBeeps(mock_lcd):
    mock_lcd.beep = AsyncMock()
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock) as mockSleep:
        await mock_lcd.displayLetter("a")
    mockSleep.assert_awaited_once_with(mock_lcd.waitTime)
    mock_lcd.beep.assert_called_once()

@pytest.mark.asyncio
async def test_displayLetter_longWaitListItem_waitsLongTimeAndDoesntBeep(mock_lcd):
    mock_lcd.beep = MagicMock()
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock) as mockSleep:
        await mock_lcd.displayLetter("!")
    mockSleep.assert_awaited_once_with(mock_lcd.longWaitTime)
    mock_lcd.beep.assert_not_called()
