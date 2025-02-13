from flask import Blueprint, jsonify, request
from app.users_authentication.models import User
from app import db
from datetime import datetime, timezone


users_authentication = Blueprint('users_authentication', __name__)


@users_authentication.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@users_authentication.route('/register', methods=['POST'])
def create_user():
    data = request.get_json() 

    required_keys = ['email', 'name', 'birthday', 'password']
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing data"}), 400

    new_user = User(
        email=data['email'],
        name=data['name'],
        birthday=datetime.strptime(data['birthday'], '%Y-%m-%d'),
        hashed_password=data['password'],
        created_at=datetime.now(timezone.utc)
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
