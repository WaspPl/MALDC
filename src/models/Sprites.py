from pydantic import BaseModel, Field

class Sprites(BaseModel):
    """
    A model for storing presaved sprites
    """
    random: dict = Field(default_factory=lambda: {
        "common": [],
        "uncommon": [],
        "rare": []
    })

    onOff: dict = Field(default_factory=lambda: {
        "on": None,
        "off": None
    })

    speech: dict = Field(default_factory=lambda: {
        "a": None,
        "m": None,
        "o": None
    })

    rest: dict = Field(default_factory=lambda: {
        "neutral": {"eyes": None, "mouth": None},
        "angry": {"eyes": None, "mouth": None},
        "sad": {"eyes": None, "mouth": None},
        "happy": {"eyes": [], "mouth": None},
    })