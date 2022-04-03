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


@db_session
def add_token(unique_hash: str, media_url: str, owner: str):
    Token(unique_hash=unique_hash, media_url=media_url, owner=owner)


@db_session
def add_tx_hash_to_token(unique_hash: str, tx_hash: str):
    token = Token.get(unique_hash=unique_hash)
    token.tx_hash = tx_hash


@db_session
def get_token_from_unique_hash(unique_hash: str):
    return Token.get(unique_hash=unique_hash)
