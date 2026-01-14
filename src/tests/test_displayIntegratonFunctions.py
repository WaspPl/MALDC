import pytest
import src.scripts.displayIntegrationFunctions as dif
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
