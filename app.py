# save this as app.py
# save this as app.py
from flask import Flask
from routes.movies_bp import movies_bp
from config import Config
from extensions import db
from sqlalchemy.sql import text


app = Flask(__name__)
app.config.from_object(Config)  # URL

db.init_app(app)


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

