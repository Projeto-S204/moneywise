from datetime import datetime, timezone
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from config import db, login_manager

bcrypt = Bcrypt()


class User(db.Model, UserMixin):
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
        return f'<User {self.name} ID {str(self.id)}>'

    def __str__(self):
        return f'{self.name}'

    def to_dict(self):
        return {
            'id': self.id,
            'avatar': self.avatar,
            'name': self.name,
            'email': self.email,
            'birthday': self.birthday.strftime('%Y-%m-%d'),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __init__(self, email, name, password, birthday,
                 avatar=None):
        self.email = email
        self.name = name
        self.hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        self.birthday = birthday
        self.avatar = avatar

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
