# save this as app.py
# save this as app.py
from flask import Flask
from routes.movies_bp import movies_bp
from routes.users_bp import users_bp
from config import Config
from extensions import db,jwt
from sqlalchemy.sql import text
from flask_cors import CORS

HTTP_UNAUTHORIZED = 401


app = Flask(__name__)
CORS(app)

app.config.from_object(Config)  # URL





db.init_app(app)
jwt.init_app(app)


@jwt.unauthorized_loader
def unauth(e):
     return {"error": "missing/invalid token"}, HTTP_UNAUTHORIZED



@jwt.expired_token_loader
def _expired(h, p):
    return ({"error": "token expired"}), HTTP_UNAUTHORIZED

with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
    except Exception as e:
        print("Error connecting to the database:", e)


@app.route("/")
def hello():
    return "<h1>Hello, World! 🎉 🔥</h1>"


HTTP_NOT_FOUND = 404

app.register_blueprint(movies_bp, url_prefix="/api/movies")
app.register_blueprint(users_bp, url_prefix="/api/auth")
