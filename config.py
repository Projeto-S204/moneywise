from socket import socket
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from flask_mail import Mail
from datetime import timedelta

DB_HOST = "db_container"
DB_NAME = "moneywise"
DB_USER = "postgres"
DB_PASS = "meritopg"
DB_PORT = "5432"

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://postgres:{DB_PASS}@{DB_HOST}/{DB_NAME}'
    )
    SECRET_KEY = (
        "k\x8d-\xbd\xb9\x05\xeax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6"
        "\xa8\x14\xf9\x89t"
    )

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'suportemw011@gmail.com'
    MAIL_PASSWORD = 'krofvxeymfmvsjwx'
    MAIL_DEFAULT_SENDER = 'suportemw011@gmail.com'
    SECURITY_PASSWORD_SALT = "7f2e1c9d3b4a6f8e"

    JWT_SECRET_KEY = (
        "k\x8d-\xbd\xb9\x04\xfax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6"
        "\xa8\x14\xf9\x89t"
    )

    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_NAME = "access_token_cookie"
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/auth/refresh'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

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
            current_port = s.getsockname()[1]

        os.environ["CURRENT_PORT"] = str(current_port)

        env_path = ".env"
        lines = []
        found = False

        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if line.startswith("CURRENT_PORT="):
                        lines.append(f"CURRENT_PORT={current_port}\n")
                        found = True
                    else:
                        lines.append(line)
        if not found:
            lines.append(f"CURRENT_PORT={current_port}\n")

        with open(env_path, "w") as f:
            f.writelines(lines)

        return current_port
