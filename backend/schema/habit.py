from pydantic import BaseModel, Field
from typing import Optional


class HabitCreateSchema(BaseModel):
    habit_name: str = Field(..., max_length=100)
    habit_type:  str = Field(..., max_length=15)
    description:  str = Field(..., max_length=100)

class HabitSchema(BaseModel):
    habit_id: Optional[int] = None
    habit_name: Optional[str] = None
    habit_type:  Optional[str] = None
    description:  Optional[str] = None