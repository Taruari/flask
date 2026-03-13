from flask import Blueprint, request
from models.user import User
from extensions import db
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500
HTTP_USER_ERROR = 400
HTTP_CREATED = 201


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

    try:
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)  # temp
        db.session.commit()

    except Exception as err:
        db.session.rollback()
        return {"message": str(err)}, HTTP_SERVER_ERROR

    return {
        "data": {"id": new_user.id, "username": new_user.username},
        "message": "User Signed up successfully",
    }, HTTP_CREATED


@users_bp.post("/login")
def users_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    stmt = select(User).where(User.username == username)
    db_user = db.session.execute(stmt).scalar_one_or_none()

    if not db_user:
        return {"error": "Invalid credentials"}, HTTP_USER_ERROR

    if not check_password_hash(db_user.password, password):
        return {"error": "Invalid credentials"}, HTTP_USER_ERROR

    token = create_access_token(identity=username)
    return {"message": "Login Successful", "token": token}
