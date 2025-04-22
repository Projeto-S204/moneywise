from socket import socket
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

DB_HOST = "localhost"
DB_NAME = "moneywise"
DB_USER = "postgres"
DB_PASS = "1234"
DB_PORT = "5432"

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{DB_PASS}@localhost/{DB_NAME}'
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

    @staticmethod
    def find_available_port():
        with socket() as s:
            s.bind(("", 0))
            return s.getsockname()[1]
