from flask import Blueprint, jsonify, request
from app.users_authentication.models import User
from app import db
from datetime import datetime
from werkzeug.security import check_password_hash
from app.users_authentication.utils import create_jwt, verify_jwt


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

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        email=data['email'],
        name=data['name'],
        birthday=datetime.strptime(data['birthday'], '%Y-%m-%d'),
        hashed_password=data['password'],
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            new_user.to_dict(),
            {'message': 'Usuário Criado com Sucesso'}
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@users_authentication.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.hashed_password, data['password']):
        token = create_jwt(user.id)
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@users_authentication.route('/protected', methods=['GET'])
def protected_route():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 403

    payload = verify_jwt(token)
    if not payload:
        return jsonify({'error': 'Token is invalid or expired'}), 403
    return jsonify({'message': 'Protected content accessed'}), 200
