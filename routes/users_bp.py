from flask import Blueprint, request
from models.user import User
from extensions import db
from sqlalchemy import select

HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 505
HTTP_USER_ERROR = 500



users_bp = Blueprint("users_bp", __name__)


@users_bp.post("/signup")
def users_details():

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


# try:
#         db.session.add(new_user)  # temp
#         db.session.commit()  # permanent

# except Exception as err:
#         db.session.rollback()  # Undo
#       return {"message": str(err)}, HTTP_SERVER_ERROR

#    return {"data": new_user.to_dict(), "message": "user is  added successfully"}


#     empty_data = []
#     for movie in data:
#         empty_data.append(movie.to_dict())

#     return empty_data


# # get//////////////////////////////
# @movies_bp.get("/<id>")
# def get_movie_by_id(id):
#     # for movie in movies:
#     #     if movie["id"] == id:
#     #         return movie
#     # return "movie not found", 404
#     data = db.session.get(Movie, id)
#     if not data:
#         return {"message": "movie not found"}, 404
#     return data.to_dict()


# # delete////////////////////
# @movies_bp.delete("/<id>")
# def delete_movie_by_id(id):
#     for movie in movies:
#         if movie["id"] == id:
#             movies.remove(movie)
#             return {"data": movie, "message": "movie delete successfully"}
#     return {"message": "movie not found"}, HTTP_NOT_FOUND


# @movies_bp.post("/")
# def create_movie():
#     # Data -> body as json
#     data = request.get_json()

#     new_movie = Movie(
#         name=data.get("name"),
#         poster=data.get("poster"),
#         summary=data.get("summary"),
#         rating=data.get("rating"),
#         trailer=data.get("trailer"),
#     )

#     try:
#         db.session.add(new_movie)  # temp
#         db.session.commit()  # permanent

#     except Exception as err:
#         db.session.rollback()  # Undo
#         return {"message": str(err)}, HTTP_SERVER_ERROR

#     return {"data": new_movie.to_dict(), "message": "movie added successfully"}


# @movies_bp.put("/<id>")
# def update_movie(id):
#     # Data -> body as json
#     update_movie = request.get_json()

#     db_movie = db.session.get(Movie, id)

#     if not db_movie:
#         return {"message": "movie not found"}, HTTP_NOT_FOUND

#     # Avenger 3
#     db_movie.name = update_movie.get("name")
#     db_movie.poster = update_movie.get("poster")
#     db_movie.summary = update_movie.get("summary")  # None
#     db_movie.rating = update_movie.get("rating")
#     db_movie.trailer = update_movie.get("trailer")  # None

#     try:
#         db.session.commit()  # permanent
#     except Exception as err:
#         db.session.rollback()  # Undo
#         return {"message": str(err)}, HTTP_SERVER_ERROR

#     return {"data": db_movie.to_dict(), "message": "movie updated successfully"}
