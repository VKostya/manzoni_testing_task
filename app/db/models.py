from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="manzoni_db", create_db=True)


class Token(db.Entity):
    id = PrimaryKey(int, auto=True)
    unique_hash = Required(str, unique=True)
    tx_hash = Optional(str, unique=True)
    media_url = Required(str)
    owner = Required(str)


sql_debug(True)
db.generate_mapping(create_tables=True)
