from fastapi import FastAPI
from handlers import router
import os


def get_app():
    app = FastAPI()
    app.include_router(router, prefix="/token")
    return app
