import os
import threading
from flask import Flask

from models import db
from add_data import add_openhours, add_rooms, add_week_schedule
from add_movies import add_movies_popular, add_movies_old
from scheduler import create_schedule_hall1, create_schedule_hall2

# Simpele setup met een sqlite database
def create_app():
    app = Flask(__name__)

    # Om de database buiten de api folder te krijgen
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    db_path = os.path.join(BASE_DIR, "CMS.db")
    
    # Link naar de database
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    
    db.init_app(app)

    from routes import bp
    app.register_blueprint(bp)

    return app


app = create_app()

# Dit zijn de achterground taken voor de threads
# Ik heb ze verdeeld om zo de load te verdelen en zodat onderdelen niet
# op elkaar hoeven te wachten
def background_movie_fetch():
    with app.app_context():
        add_movies_popular()
        add_movies_old()
        add_week_schedule()

def schedule_movie1():
    with app.app_context():
        create_schedule_hall1()

def schedule_movie2():
    with app.app_context():
        create_schedule_hall2()
    

# Maak de database en tabellen vul de data en begin de achterground processen
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        add_rooms()
        add_openhours()

    # Dit zijn de runnende achtergrond taken, ideal zijn ze niet op deze locatie
    # Dit had beter een los process kunnen zijn
    threading.Thread(target=background_movie_fetch, daemon=True).start()
    threading.Thread(target=schedule_movie1, daemon=True).start()
    threading.Thread(target=schedule_movie2, daemon=True).start()

    app.run(debug=True)
