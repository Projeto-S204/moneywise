from socket import socket
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager

DB_HOST = "localhost"
DB_NAME = "moneywise"
DB_USER = "postgres"
DB_PASS = "1234"
DB_PORT = "5432"

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://postgres:{DB_PASS}@localhost/{DB_NAME}'
    )
    SECRET_KEY = (
        "k\x8d-\xbd\xb9\x05\xeax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6"
        "\xa8\x14\xf9\x89t"
    )

    @staticmethod
    def find_available_port():
        with socket() as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    @staticmethod
    def get_db_connection():
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        return conn
