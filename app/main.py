from tracemalloc import start
from fastapi import FastAPI
from handlers import router
import os


app = FastAPI()
app.include_router(router, prefix="/tokens")
