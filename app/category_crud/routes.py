from flask import Blueprint, request
from app.category_crud.category_db import (
    get_categories as get_categories_db,
    get_category as get_category_db,
    create_category as create_category_db,
    update_category as update_category_db,
    delete_category as delete_category_db
)

category_crud = Blueprint('category_crud', __name__)

@category_crud.route('/categories', methods=['GET'])
def get_categories():
    return get_categories_db()

@category_crud.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return get_category_db(category_id)

@category_crud.route('/category', methods=['POST'])
def create_category():
    return create_category_db(request)

@category_crud.route('/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    return update_category_db(category_id, request)

@category_crud.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    return delete_category_db(category_id)
