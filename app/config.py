import os


class Config:
    DEBUG = os.getenv("DEBUG", True)

    HOST = os.getenv("SERVICE_HOST", "127.0.0.1")
    PORT = os.getenv("SERVICE_PORT", 8000)

    ABI = os.getenv("ABI")
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

    DB_PROVIDER = os.getenv("DB_PROVIDER", "sqlite")
    DB_NAME = os.getenv("DB_NAME", "manzoni_db")

    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    ENDPOINT = os.getenv("ENDPOINT")


config = Config()
