import uvicorn
import os

import database.table_diagrams as td

from fastapi import FastAPI

from contextlib import asynccontextmanager
from database.connection import JobDb
from servise.router import router

from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await JobDb().create_pool()
    yield
    await JobDb().close_pool()



app = FastAPI(
    lifespan=lifespan,
    title='Сервис регистрации/авторизации пользователя',
    version='0.0.1')

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))


