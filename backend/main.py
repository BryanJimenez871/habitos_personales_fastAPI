from .routers import habit_router, daily_router, date_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .connection.connection_db import ConnectionDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    await ConnectionDB.get_pool()
    yield
    # SHUTDOWN
    await ConnectionDB.close_pool()

app = FastAPI(
    title="Proyecto API",
    version="1.0.0",
    lifespan=lifespan
)

# routers
app.include_router(habit_router)
app.include_router(daily_router)

app.include_router(date_router)