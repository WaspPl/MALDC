import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock, patch

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
def mock_lcd():
    lcd = MagicMock()
    lcd.create_char.return_value = 0
    lcd.write_string.return_vaslue = 0
    return lcd

def test_beep_GPIOGetsTurnedOn(mock_lcd, mock_GPIO):


    lcd = LCD(mock_lcd, mock_GPIO)

    lcd.beep()
    mock_GPIO.output.assert_any_call(lcd.buzzerPin, mock_GPIO.LOW)
    
def test_beep_GPIOGetsTurnedOff(mock_lcd, mock_GPIO):


    lcd = LCD(mock_lcd, mock_GPIO)

    lcd.beep()


    mock_GPIO.output.assert_any_call(lcd.buzzerPin, mock_GPIO.HIGH)
def test_beep_GPIOgoesOnAndThenOff(mock_lcd, mock_GPIO):

    from unittest.mock import call

    lcd = LCD(mock_lcd, mock_GPIO)

    lcd.beep()

    calls = mock_GPIO.output.call_args_list
    #The 0th is the setup call
    assert calls[1] == call(lcd.buzzerPin, mock_GPIO.LOW)
    assert calls[2] == call(lcd.buzzerPin, mock_GPIO.HIGH)

@pytest.mark.asyncio
async def test_displayLeter_writesOnlyOneLetter(mock_lcd, mock_GPIO):
    #Arrange
    lcd = LCD(mock_lcd,mock_GPIO)
    #Act
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock) as mockSleep:
        await lcd.displayLetter("x")
    #Assert
    mock_lcd.write_string.assert_called_once_with("x")
    

@pytest.mark.asyncio
async def test_displayLeter_waitsNormalTimeWhenDisplayingASpaceAndDoesntBeep(mock_lcd, mock_GPIO):
    #Arrange
    lcd = LCD(mock_lcd,mock_GPIO)
    lcd.beep = MagicMock()
    #Act
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock) as mockSleep:
        await lcd.displayLetter(" ")
    #Assert
        mockSleep.assert_awaited_once_with(lcd.waitTime)
        lcd.beep.assert_not_called()
    

@pytest.mark.asyncio
async def test_displayLeter_waitsNormalTimeWhenDisplayingALetterAndBeeps(mock_lcd, mock_GPIO):
        #Arrange
    lcd = LCD(mock_lcd,mock_GPIO)
    lcd.beep = MagicMock()
    #Act
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock) as mockSleep:
        await lcd.displayLetter("a")
    #Assert
        mockSleep.assert_awaited_once_with(lcd.waitTime)
        lcd.beep.assert_called_once()


@pytest.mark.asyncio
async def test_displayLeter_waitsLongTimeWhenDisplayingACharacterFromTheLongWaitListAndDoesntBeep(mock_lcd, mock_GPIO):
        #Arrange
    lcd = LCD(mock_lcd,mock_GPIO)
    lcd.beep = MagicMock()
    #Act
    with patch("src.controllers.LCDAndBuzzerController.asyncio.sleep", new_callable=AsyncMock) as mockSleep:
        await lcd.displayLetter("!")
    #Assert
        mockSleep.assert_awaited_once_with(lcd.longWaitTime)
        lcd.beep.assert_not_called()

