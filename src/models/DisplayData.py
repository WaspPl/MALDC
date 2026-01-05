from pydantic import BaseModel, Base64Str

class DisplayData(BaseModel):
    """Data used to receive and display things sent over to the API"""
    message: str
    sprite: Base64Str = None
    spriteReplayTimes: int = 1

    