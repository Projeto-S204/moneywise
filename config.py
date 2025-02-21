import os
from socket import socket

BASEDIR = os.path.dirname(os.path.abspath("app.py"))


def find_available_port():
    with socket() as s:
        s.bind(("", 0))
        print(s.getsockname())
        return s.getsockname()[1]


class Config:
    FLASK_DEBUG = 1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://postgres:meritopg@localhost/dashboard'
    )
    SECRET_KEY = (
        "k\x8d-\xbd\xb9\x05\xeax\x92\xd9{H\xf0\x9c\xf9\xde\x91\xc6\xe6"
        "\xa8\x14\xf9\x89t"
    )

    JWT_SECRET_KEY = SECRET_KEY
