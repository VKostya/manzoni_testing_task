from pony.orm import PrimaryKey, Required, Optional

from ..main import db


class Token(db.Entity):
    id = PrimaryKey(int, auto=True)
    unique_hash = Required(str, unique=True)
    tx_hash = Optional(str, unique=True)
    media_url = Required(str)
    owner = Required(str)


db.generate_mapping(create_tables=True)
