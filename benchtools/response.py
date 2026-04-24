from pydantic import BaseModel
from enum import Enum

class StringAnswer(BaseModel):
    '''
    simple string in an 'answer' key
    '''
    answer: str
    
class IntAnswer(BaseModel):
    answer: int

class FloatAnswer(BaseModel):
    answer: float

class StringJustification(BaseModel):
    answer: str
    justification: str 

class IntJustification(BaseModel):
    answer: int
    justification: str 

class SentimentEnum(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class YesNoEnum(str,Enum):
    yes = "yes"
    no = "no"

class Binary(BaseModel):
    answer: YesNoEnum

class BinaryJustification(BaseModel):
    answer: YesNoEnum
    justification: str 