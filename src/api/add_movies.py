import os
import requests
import time
from dotenv import load_dotenv

from models import Movie, db
from sqlalchemy.exc import IntegrityError

load_dotenv()

API_KEY = os.getenv("API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Check for the unique contraints
def unique_movie(external_id):
    unique_movie = Movie.query.filter_by(external_id=external_id).first()
    if not unique_movie:
        return True
    else:
        return False

# Make function to add the movies to the database
def add_movies_popular():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-NL&page=1&release_date.gte=1995-01-02&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=2000"
    response = requests.get(url, headers=headers)
    result = response.json()
    pages = result["total_pages"]

    # Per page add movies to the database
    for page in range(1, pages):
    
        # Get the movies from themoviedb in dutch
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-NL&page={page}&release_date.gte=1995-01-02&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=2000"
        response = requests.get(url, headers=headers)
        result = response.json()
        movies = result["results"]
        
        for movie in movies:
            external_id = movie["id"]
            title_nl = movie["title"]
            description_nl = movie["overview"]

            # To filter movies for hall 1
            rating = movie["vote_average"]
            popularity = movie["popularity"]

            # Get the additional runtime information
            if external_id and title_nl and description_nl and unique_movie(external_id): 
                url = f"https://api.themoviedb.org/3/movie/{external_id}?language=nl-NL"
                response = requests.get(url, headers=headers)
                data = response.json()
                # To calculate the daily schedule
                runtime_minutes = data["runtime"]
                # To filter movies for hall 2
                release_date = data["release_date"]

                # Add the movie to the database
                new_movie = Movie(
                    external_id=external_id,
                    title_nl=title_nl,
                    description_nl=description_nl,
                    runtime_minutes=runtime_minutes,
                    release_date=release_date,
                    rating=rating,
                    popularity=popularity
                )
                db.session.add(new_movie)
                try:
                    db.session.commit()
                    print(f"Movie with ID: {external_id}, added!")
                except IntegrityError:
                    db.session.rollback()
                    print(f"Movie {title_nl} already exists, skipping...")
                time.sleep(0.25)


def add_movies_old():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-EN&page=1&release_date.lte=1995-01-01&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=100"
    response = requests.get(url, headers=headers)
    result = response.json()
    pages = result["total_pages"]

    # Scan trough movie list to filter popular movies
    for page in range(1, pages):
    
        # Get the movies from themoviedb in dutch
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-EN&page={page}&release_date.lte=1995-01-01&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=100"
        response = requests.get(url, headers=headers)
        result = response.json()
        movies = result["results"]
        
        for movie in movies:
            external_id = movie["id"]
            title_nl = movie["title"]
            description_nl = movie["overview"]

            # To filter movies for hall 1
            rating = movie["vote_average"]
            popularity = movie["popularity"]

            # Get the additional runtime information
            if external_id and title_nl and description_nl and unique_movie(external_id, title_nl): 
                url = f"https://api.themoviedb.org/3/movie/{external_id}?language=nl-NL"
                response = requests.get(url, headers=headers)
                data = response.json()

                # To calculate the daily schedule
                runtime_minutes = data["runtime"]
                # To filter movies for hall 2
                release_date = data["release_date"]

                # Add the movie to the database
                new_movie = Movie(
                    external_id=external_id,
                    title_nl=title_nl,
                    description_nl=description_nl,
                    runtime_minutes=runtime_minutes,
                    release_date=release_date,
                    rating=rating,
                    popularity=popularity
                )
                db.session.add(new_movie)
                try:
                    db.session.commit()
                    print(f"Movie with ID: {external_id}, added!")
                except IntegrityError:
                    db.session.rollback()
                    print(f"Movie {title_nl} already exists, skipping...")
                time.sleep(0.25)
