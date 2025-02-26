import psycopg2
import os

class Config:
    SECRET_KEY = "k\x8d-\xbd\xb9\x05\xeax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6\xa8\x14\xf9\x89t"
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
        
    @staticmethod
    def get_db_connection():
        database_url = SQLALCHEMY_DATABASE_URI
        
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        return conn