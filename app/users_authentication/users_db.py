# from flask import jsonify, request
# from app.users_authentication.models import User
# from app import db
# from datetime import datetime
# from werkzeug.security import check_password_hash
# from app.users_authentication.utils import create_jwt


# def get_users():
#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users])


# def get_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify(user.to_dict())


# def create_user(request):
#     data = request.get_json()

#     existing_user = User.query.filter_by(email=data['email']).first()
#     if existing_user:
#         return jsonify({"error": "Email already registered"}), 400

#     new_user = User(
#         email=data['email'],
#         name=data['name'],
#         birthday=datetime.strptime(data['birthday'], '%Y-%m-%d'),
#         # password=data['password'],
#     )

#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify(
#             new_user.to_dict(),
#             {'message': 'Usuário Criado com Sucesso'}
#         ), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


# def login_user(request):
#     data = request.get_json()

#     if 'email' not in data or 'password' not in data:
#         return jsonify({"error": "Missing email or password"}), 400

#     user = User.query.filter_by(email=data['email']).first()

#     if user and check_password_hash(user.hashed_password, data['password']):
#         token = create_jwt(user.id)
#         return jsonify({'message': 'Login successful', 'token': token}), 200
#     else:
#         return jsonify({"error": "Invalid email or password"}), 401


# def update_user(user_id):
#     data = request.get_json()

#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     if 'name' in data:
#         user.name = data['name']

#     if 'avatar' in data:
#         user.avatar = data['avatar']

#     try:
#         db.session.commit()
#         return jsonify({
#             "message": "User updated successfully",
#             "user": user.to_dict()
#         }), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     try:
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({"message": "User deleted successfully"}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


# # Rota para teste do token
# # @users_authentication.route('/protected', methods=['GET'])
# # def protected_route():
# #     token = request.headers.get('Authorization')
# #     if not token:
# #         return jsonify({'error': 'Token is missing'}), 403

# #     payload = verify_jwt(token)
# #     if not payload:
# #         return jsonify({'error': 'Token is invalid or expired'}), 403
# #     return jsonify({'message': 'Protected content accessed'}), 200
