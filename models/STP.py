from pydantic import BaseModel
from models.QuaterLevels import QuaterLevels
from models.StaticLevels import StaticLevels


class STP(BaseModel):
    static_water_level: int | float
    pump_setting: int | float
    buffer_: int | float
    StaticLevel: StaticLevels
    QuaterLevel: QuaterLevels
    