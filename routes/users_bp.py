from flask import Blueprint, request
from models.user import User
from extensions import db
from sqlalchemy import select

HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 505
HTTP_USER_ERROR = 500



users_bp = Blueprint("users_bp", __name__)


@users_bp.post("/signup")
def users_signup():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    stmt = select(User).where(User.username == username)
    db_user = db.session.execute(stmt).scalars().all()

    if db_user:
        return {"error": "username already taken"}, HTTP_USER_ERROR

    new_user = User(username=username, password=password)
    db.session.add(new_user)  # temp
    db.session.commit()
    return new_user.to_dict()



@users_bp.post("/login")
def users_login():
    data= request.get_json()
    username = data.get("username")
    password = data.get("password")

    stmt = select(User).where(User.username == username)
    db_user = db.session.execute(stmt).scalar_one_or_none()

    if not db_user:
        return {"error": "Invalid credentials"}, HTTP_USER_ERROR

    if db_user.password != password:
     return {"error": "Invalid credentials"}, HTTP_USER_ERROR
    
    return {"message": "Login Successful"}

    
