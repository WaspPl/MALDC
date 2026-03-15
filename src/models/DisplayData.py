from pydantic import BaseModel
from typing import Optional

class DisplayData(BaseModel):
    """Data used to receive and display things sent over to the API"""
    message: Optional[str] = None
    spriteBase64: Optional[str] = None
    spriteReplayTimes: int = 1

    