from flask import Blueprint, request
from app.users_authentication.users_db import (
    get_users_db,
    get_user_db,
    create_user_db,
    login_user_db,
    update_user_db,
    delete_user_db
)


users_authentication = Blueprint('users_authentication', __name__)


@users_authentication.route('/users', methods=['GET'])
def get_users():
    return get_users_db()


@users_authentication.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return get_user_db(user_id)


@users_authentication.route('/users', methods=['POST'])
def create_user():
    return create_user_db(request)


@users_authentication.route('/login', methods=['POST'])
def login_user():
    return login_user_db(request)


@users_authentication.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return update_user_db(user_id, request)


@users_authentication.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return delete_user_db(user_id)
