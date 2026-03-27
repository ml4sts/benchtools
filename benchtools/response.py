from pydantic import BaseModel


class StringAnswer(BaseModel):
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