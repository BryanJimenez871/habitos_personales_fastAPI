from datetime import date
from fastapi import APIRouter, HTTPException, status

from app import crud, schema

router = APIRouter(prefix="/dates", tags=["Date"])


@router.post("/", response_model=schema.DateSchema)
async def insert_habit(date: schema.DateCreateSchema):
    new_id = await crud.DateCrud.insert_date(date)
    return schema.DateSchema(date_id=new_id, **date.model_dump())


@router.get("/", response_model=int | None)  # EL none, porque aveces la fecha no existe
async def get_date_id(habit_date: date):
    date_id = await crud.DateCrud.search_date(habit_date)
    return date_id


@router.get("/range/", response_model=list[schema.DailyHabitsSchema])
async def get_pie_chart(start_date: date, end_date: date):
    pie_chart = await crud.DateCrud.select_range_date(start_date, end_date)
    if pie_chart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return pie_chart

@router.get("/day_pie_chart/", response_model=list[schema.DailyHabitsSchema])
async def get_pie_chart(start_date: date):
    pie_chart = await crud.DateCrud.select_only_day(start_date)
    if pie_chart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return pie_chart

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_date():
    await crud.DateCrud.delete_all()

@router.delete("/date_id_deleted/{date_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_date(date_id: int):
    await crud.DateCrud.delete_date_id(date_id)
