from pydantic import BaseModel
from typing import Optional

from app import schema


# Post -> input, lo que envio de json al servidor api
class DailyHabitsCreateSchema(BaseModel):
    habit: schema.HabitSchema
    date: schema.DateSchema
    complet: bool

# Get/Post -> output # lo que responde y envio a base de datos
class DailyHabitsSchema(BaseModel):
    daily_id: Optional[int] = None
    habit: Optional[schema.HabitSchema] = None
    date: Optional[schema.DateSchema] = None
    complet: Optional[bool] = None

