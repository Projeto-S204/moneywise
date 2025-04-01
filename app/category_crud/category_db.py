from flask import jsonify
from app import db
from app.category_crud.models import Category

def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category.to_dict())

def create_category(request):
    data = request.get_json()

    if 'name' not in data or 'color' not in data:
        return jsonify({"error": "Missing name or color"}), 400

    existing_category = Category.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({"error": "Category already exists"}), 400

    new_category = Category(name=data['name'], color=data['color'])

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.to_dict(), {'message': 'Category created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def update_category(category_id, request):
    data = request.get_json()

    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    if 'name' in data:
        category.name = data['name']
    if 'color' in data:
        category.color = data['color']

    try:
        db.session.commit()
        return jsonify({"message": "Category updated successfully", "category": category.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
