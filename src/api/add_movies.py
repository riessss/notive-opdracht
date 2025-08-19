import os
import requests
import time
from dotenv import load_dotenv
from datetime import datetime

from models import Movie, db
from sqlalchemy.exc import IntegrityError

# Gekozen voor een dotenv file voor al ik de code zou delen op github
# Ik heb de key toegevoegd aan de headers en deze meegestuurd met de request
load_dotenv()
API_KEY = os.getenv("API_KEY")
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Dit is een helper functie voor het checken van unieke_ids
# Ik had hier eers ook de titel bij maar dit zorgde er voor dat ik geen data in kon laden
# omdat er veel dubbele titels waren. Dit heb ik uiteindelijk niet meer uit kunnen zoeken
# omdat ik druk was met het maken van de volgende stappen.
def unique_movie(external_id):
    unique_movie = Movie.query.filter_by(external_id=external_id).first()
    if not unique_movie:
        return True
    else:
        return False

# Om te voorkomen dat de code hardcoded data bevat heb ik hier de api gecalled voor de page lengte
# Ik heb gekozen voor twee functies om zo een betere splitsing tussen de twee zalen te hebben
def add_movies_popular():
    # Hier heb ik via de themoviedb gefiltert op de films om te veel API calls te verkomen'
    # Dit betekent dat ik de andere 
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-NL&page=1&release_date.gte=1995-01-02&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=2000"
    response = requests.get(url, headers=headers)
    result = response.json()
    pages = result["total_pages"]

    # Per pagina de data naar de database verstuurd
    for page in range(1, pages):
    
        # De pagina's als f string toegevoegd om zo door de paginas te gaan
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-NL&page={page}&release_date.gte=1995-01-02&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=2000"
        response = requests.get(url, headers=headers)

        # Ik heb gekozen voor data als json om zo makkelijk verchillende data te selecteren
        result = response.json()
        movies = result["results"]
        
        for movie in movies:
            external_id = movie["id"]
            title_nl = movie["title"]
            description_nl = movie["overview"]

            # Deze heb ik hier toegevoegd om zo te kunnen filteren voor de populaire films
            rating = movie["vote_average"]
            popularity = movie["popularity"]

            # Om null data te voorkomen en geen dubbele external_ids te hebben
            # Zodat de database gezond blijft 
            if external_id and title_nl and description_nl and unique_movie(external_id): 

                # Hier heb ik nog een keer de API gecalld om zo de duur van de film te krijgen
                url = f"https://api.themoviedb.org/3/movie/{external_id}?language=nl-NL"
                response = requests.get(url, headers=headers)
                data = response.json()

                # Ik heb dit als integer in de database gestopt
                # Dit had ook als time in de database kunnen gaan om complexiteit te verminderen in scheduler.py
                runtime_minutes = data["runtime"]
                
                # 
                release_date_str = data["release_date"]  
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()

                # De films toegevoed aan de database en gekeken naar integrety errors in de database
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

                # Om rekening the houden met het roepen van de API
                time.sleep(0.25)


# Hetzelfde als de andere functie
# Alleen de filters zijn anders in deze functie
def add_movies_old():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-EN&page=1&release_date.lte=1995-01-01&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=100"
    response = requests.get(url, headers=headers)
    result = response.json()
    pages = result["total_pages"]

    for page in range(1, pages):
        # Andre filter dan bij popular movies
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=nl-EN&page={page}&release_date.lte=1995-01-01&sort_by=popularity.desc&vote_average.gte=8&vote_count.gte=100"
        response = requests.get(url, headers=headers)
        result = response.json()
        movies = result["results"]
        
        for movie in movies:
            external_id = movie["id"]
            title_nl = movie["title"]
            description_nl = movie["overview"]

            rating = movie["vote_average"]
            popularity = movie["popularity"]

            if external_id and title_nl and description_nl and unique_movie(external_id): 
                url = f"https://api.themoviedb.org/3/movie/{external_id}?language=nl-NL"
                response = requests.get(url, headers=headers)
                data = response.json()

                runtime_minutes = data["runtime"]

                release_date_str = data.get("release_date")
                release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()

                
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
