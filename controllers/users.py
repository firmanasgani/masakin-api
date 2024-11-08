from flask import Blueprint, request

from connectors.mysql_connector import connection
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