from dataclasses import dataclass

import psycopg2
from psycopg2.extras import DictCursor

@dataclass
class DBConfig:
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

config = DBConfig(
    DB_NAME="tcc",
    DB_USER="alexandremj",
    DB_PASSWORD="test_password",
    DB_HOST="localhost",
    DB_PORT="5432",
)

def connect_db():
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        cursor_factory=DictCursor
    )
