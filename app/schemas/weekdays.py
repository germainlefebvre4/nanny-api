from typing import Optional
from datetime import time

from pydantic import BaseModel


class DayHourBase(BaseModel):
    start: time
    end: time


class DayHour(DayHourBase):
    pass


class WeekdaysBase(BaseModel):
    enabled: bool = False
    monday: Optional[DayHour]
    tuesday: Optional[DayHour]
    wednesday: Optional[DayHour]
    thursday: Optional[DayHour]
    friday: Optional[DayHour]
    saturday: Optional[DayHour]
    sunday: Optional[DayHour]


class Weekdays(WeekdaysBase):
    pass
