from fastapi import FastAPI
from dotenv import dotenv_values
import os

app = FastAPI()


@app.get("/")
async def root():
    return dotenv_values(".env")