from socket import socket
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv

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

    # If you are using playwright, please make sure to set debug=False
    @staticmethod
    def find_available_port():
        with socket() as s:
            s.bind(("", 0))
            available_port = s.getsockname()[1]

        os.environ["AVAILABLE_PORT"] = str(available_port)

        env_path = ".env"
        lines = []
        found = False

        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if line.startswith("AVAILABLE_PORT="):
                        lines.append(f"AVAILABLE_PORT={available_port}\n")
                        found = True
                    else:
                        lines.append(line)
        
        if not found:
            lines.append(f"AVAILABLE_PORT={available_port}\n")

        with open(env_path, "w") as f:
            f.writelines(lines)

        return available_port
