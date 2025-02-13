from datetime import datetime, timezone
from app import db

# Criação da tabela de usuários


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'

    def to_dict(self):
        return {
            'avatar': self.avatar,
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'birthday': self.birthday.strftime('%Y-%m-%d'),
            'created_at': self.created_at,

        }
