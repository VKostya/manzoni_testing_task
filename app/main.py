from fastapi import FastAPI
from pony.orm import Database, sql_debug

from api.service_api import router
from app.config import Config

config = Config()

db = Database()
db.bind(provider=config.DB_PROVIDER, filename=config.DB_NAME, create_db=True)
db.generate_mapping(create_tables=True)

if config.DEBUG:
    sql_debug(True)

app = FastAPI()
app.include_router(router, prefix="/tokens")
