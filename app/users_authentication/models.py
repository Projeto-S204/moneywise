from datetime import datetime, timezone
from app import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return (
            f'<User {self.name} ID {str(self.id)}> name= {self.name} '
            f'email= {self.email}')

    def __str__(self):
        return f'{self.name}'

    def to_dict(self):
        return {'id': self.id,
                'avatar': self.avatar,
                'name': self.name,
                'email': self.email,
                'birthday': (self.birthday.strftime('%Y-%m-%d')
                             if self.birthday else None),
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'password': self.hashed_password}

    def __init__(self, email, name, password, birthday, avatar=None):
        self.email = email
        self.name = name
        self.hashed_password = generate_password_hash(password)
        self.birthday = birthday
        self.avatar = avatar
