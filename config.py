from socket import socket
import psycopg2

DB_HOST = "database.cp6y2smecfjo.us-east-2.rds.amazonaws.com"
DB_NAME = "moneywise"
DB_USER = "postgres"
DB_PASS = "nrqakc12"
DB_PORT = "5432"

def find_available_port():
    with socket() as s:
        s.bind(("", 0))
        print(s.getsockname())
        return s.getsockname()[1]

class Config:
    FLASK_DEBUG = 1
    SECRET_KEY = "k\x8d-\xbd\xb9\x05\xeax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6\xa8\x14\xf9\x89t"

    def get_db_connection():
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
