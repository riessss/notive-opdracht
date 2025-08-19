import os
import threading
from flask import Flask, jsonify

from models import db, Room
from add_data import add_openhours, add_rooms
from add_movies import add_movies_popular, add_movies_old
# from scheduler import create_schedule_hall1, create_schedule_hall2

def create_app():
    app = Flask(__name__)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    db_path = os.path.join(BASE_DIR, "CMS.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)

    return app

app = create_app()

def background_movie_fetch():
    with app.app_context():
        add_movies_popular()
        add_movies_old()

def schedule_movies():
    with app.app_context():
        create_schedule_hall1()
        create_schedule_hall2()
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        add_rooms()
        add_openhours()

    threading.Thread(target=background_movie_fetch, daemon=True).start()
    threading.Thread(target=schedule_movies, daemon=True).start()


    app.run(debug=True)
