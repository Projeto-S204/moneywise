from socket import socket
import psycopg2

DB_HOST = "localhost"
DB_NAME = "moneywise"
DB_USER = "postgres"
DB_PASS = "1234"
DB_PORT = "5432"


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://postgres:meritopg@localhost/dashboard'
    )
    SECRET_KEY = (
        "k\x8d-\xbd\xb9\x05\xeax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6"
        "\xa8\x14\xf9\x89t"
    )

    JWT_SECRET_KEY = SECRET_KEY

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
