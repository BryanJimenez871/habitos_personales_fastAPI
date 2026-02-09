from fastapi import APIRouter, HTTPException, status

from app import crud, schema

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.post("/", response_model=schema.HabitSchema)
async def insert_habit(habit: schema.HabitCreateSchema):
    new_id = await crud.HabitCrud.insert_habit(habit)
    return schema.HabitSchema(habit_id=new_id, **habit.model_dump()) # **habit.model_dump() vendría ser lo demás, habit_name, habit_type, description

@router.get("/", response_model=list[schema.HabitSchema])
async def get_habits():
    tabla = await crud.HabitCrud.select()
    if tabla is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return tabla

@router.get("/habit_name/{habit_name}", response_model=int)
async def get_habit_id(habit_name: str):
    habit_id = await crud.HabitCrud.search_name(habit_name)
    if habit_id is None:
        return None
    return habit_id

@router.delete("/habit_id_deleted/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(habit_id: int):
    await crud.HabitCrud.delete_habit(habit_id)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all():
    await crud.HabitCrud.delete_all()
