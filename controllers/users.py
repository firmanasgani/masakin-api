from flask import Blueprint, request, jsonify
from connectors.mysql_connector import connection
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

from models.users import Users

users_routes = Blueprint("users_routes", __name__)

Session = sessionmaker(connection)
s = Session()

@users_routes.route("/users/register", methods=["POST"])
def register_user():

    try:
        NewUser = Users(
            id=request.form["id"], # ini mau Generate ID pake apa ya nanti?
            email=request.form["email"],
            full_name=request.form["full_name"],
        )
        
        NewUser.set_password(request.form["password"])
        NewUser.created_at = func.now()

        if request.form["password"] != request.form["confirm_password"]:
            s.rollback()
            return {"message": "password doesn't match"}, 401
        
        s.add(NewUser)
        s.commit()
    
    except Exception as e:
        s.rollback()
        print(f"Error : {e}")
        return {"message": "Fail to register"}, 500
    
    return {"message": "Register user success"}, 200

@users_routes.route("/users/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    try:
        user = s.query(Users).filter_by(email=email).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404
        if not user.check_password(password):
            return jsonify({'message': 'Incorrect password'}), 401

        access_token = create_access_token(identity={'user_id': user.id, 'username': user.full_name})
        return jsonify({
            'message': 'User login successful',
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500

    finally:
        s.close()

@users_routes.route("/users/logout", methods=["POST"])
@jwt_required()
def logout_user():
    response = jsonify({'message': ' User Logout successful'})
    unset_jwt_cookies(response) 
    return response, 200