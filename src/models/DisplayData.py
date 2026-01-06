from pydantic import BaseModel, Base64Str
from typing import Optional

class DisplayData(BaseModel):
    """Data used to receive and display things sent over to the API"""
    message: str
    spriteBase64: Optional[str] = None
    spriteReplayTimes: int = 1

    