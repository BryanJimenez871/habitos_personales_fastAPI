from pydantic import BaseModel
from typing import Optional
from datetime import date

class DateCreateSchema(BaseModel):
    habit_date: date

class DateSchema(BaseModel):
    date_id: Optional[int] = None
    habit_date: Optional[date] = None
