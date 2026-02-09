from fastapi import APIRouter, HTTPException

from fastapi import status
from app import crud, schema

router = APIRouter(prefix="/daily_habits", tags=["DailyHabits"])

@router.post('/', response_model= schema.DailyHabitsSchema)
async def insert_daily_habit(daily_habit: schema.DailyHabitsCreateSchema):
    new_id = await crud.DailyHabitsCrud.insert_daily(daily_habit)
    return schema.DailyHabitsSchema(daily_id=new_id, **daily_habit.model_dump())

@router.get("/", response_model=list[schema.DailyHabitsSchema])
async def get_daily_habits():
    tabla = await crud.DailyHabitsCrud.select_join()
    if tabla is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return tabla

@router.get("/pie_chart/", response_model=list[schema.DailyHabitsSchema])
async def get_daily_habits_pie_chart():
    pie_chart = await crud.DailyHabitsCrud.select_pie_chart()
    if pie_chart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return pie_chart


@router.delete("/habit_id_deleted/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_id_habit(habit_id:int):
    await crud.DailyHabitsCrud.delete_id_habit(habit_id)

@router.delete("/daily_id_deleted/{daily_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_id_daily_habit(daily_id:int):
    row_deleted = await crud.DailyHabitsCrud.delete_id_daily(daily_id)
    print(f"Filas eliminadas: {row_deleted}")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_daily_habit():
    await crud.DailyHabitsCrud.delete_all()

