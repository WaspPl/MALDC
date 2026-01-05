import pytest
from unittest.mock import MagicMock

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
    return lcd

def test_buzzerTogglesGPIOCorrectly_GPIOGetsTurnedOn(mock_lcd, mock_GPIO):
    from src.controllers.LCDAndBuzzerController import LCD

    lcd = LCD(mock_lcd, mock_GPIO)

    lcd.beep()
    mock_GPIO.output.assert_any_call(lcd.buzzerPin, mock_GPIO.LOW)
    
def test_buzzerTogglesGPIOCorrectly_GPIOGetsTurnedOff(mock_lcd, mock_GPIO):
    from src.controllers.LCDAndBuzzerController import LCD

    lcd = LCD(mock_lcd, mock_GPIO)

    lcd.beep()


    mock_GPIO.output.assert_any_call(lcd.buzzerPin, mock_GPIO.HIGH)
def test_buzzerTogglesGPIOCorrectly_GPIOgoesOnAndThenOff(mock_lcd, mock_GPIO):
    from src.controllers.LCDAndBuzzerController import LCD
    from unittest.mock import call

    lcd = LCD(mock_lcd, mock_GPIO)

    lcd.beep()

    calls = mock_GPIO.output.call_args_list
    #The 0th is the setup call
    assert calls[1] == call(lcd.buzzerPin, mock_GPIO.LOW)
    assert calls[2] == call(lcd.buzzerPin, mock_GPIO.HIGH)
