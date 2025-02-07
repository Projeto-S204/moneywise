import os


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql:///moneywise_db"
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
