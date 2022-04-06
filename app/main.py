import uvicorn
from fastapi import FastAPI, APIRouter
from pony.orm import Database, sql_debug

from .api.service_api import router
from .config import config

db = Database()
db.bind(provider=config.DB_PROVIDER, filename=config.DB_NAME, create_db=True)

if config.DEBUG:
    sql_debug(True)

app = FastAPI()
app.include_router(router, prefix="/tokens")

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
