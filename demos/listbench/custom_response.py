from pydantic import BaseModel
from enum import Enum

class Direction(str,Enum):
    left="left"
    right="right"
    up="up"

class NameSource(BaseModel):
    name: str
    direction : Direction