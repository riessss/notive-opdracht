from models import (
    Movie,
    Screening,
    OpeningHour,
    WeekSchedule,
    db
)
from datetime import datetime, timedelta

from main import app

def create_schedule_hall1():
    with app.app_context():
        movies = Movie.query.filter(Movie.rating > 8).all()

        print([movie.title_nl for movie in movies])

        movie_used_id = 0

        for day in range(1, 8):
            week_day = OpeningHour.query.filter_by(id=day).first()

            opening = datetime.combine(datetime.today(), week_day.opening_time)
            closing = datetime.combine(datetime.today(), week_day.closing_time)
            
            minutes_open = (closing - opening).total_seconds() / 60

            time_left = True
            while time_left:

                runtime = movies[movie_used_id].runtime_minutes
                if minutes_open < runtime:
                    time_left = False
                
                # Check how to make it work
                runtime_time = timedelta(minutes=runtime)
                starting_time = week_day.closing_time - runtime_time
                minutes_open -= (15 + runtime)

                date = 
                room_id = 1
                week_schedule_id = 
                language = "Nederlands"

                movie_used_id += 1

                screening = Screening(
                    week_schedule_id=week_schedule_id,
                    room_id=room_id,
                    movie_id=movie_used_id,
                    date=date,
                    starting_time=starting_time,
                    language=language)

                db.session.add(screening)
                db.session.commit()


create_schedule_hall1()

def create_schedule_hall2():
    movies = Movie.query.filter().all