from pydantic import BaseModel

class StaticLevels(BaseModel):
    s1: int | float
    s2: int | float
    s3: int | float
    s4: int | float
    s5: int | float