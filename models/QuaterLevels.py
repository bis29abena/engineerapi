from pydantic import BaseModel

class QuaterLevels(BaseModel):
    q1: int | float
    q2: int | float
    q3: int | float
    q4: int | float
    q5: int | float