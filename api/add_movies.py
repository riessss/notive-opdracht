import os
import requests
from dotenv import load_dotenv
from celery import Celery, Task

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Popularity
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


for page in range(1, 51989):
    url = f"https://api.themoviedb.org/3/movie/popular?language=nl-US&page={page}&sort_by=popularity.asc"
    response = requests.get(url, headers=headers)
    result = response.json()
    movies = result["results"]
    
    for movie in result["results"]:
        if movie["vote_average"] > 8.5:
            id = movie["id"]
            title = movie["title"]
            overview = movie["overview"]
            rating = movie["vote_average"]
            popularity = movie["popularity"]
            if id and title and overview: 
                url = f"https://api.themoviedb.org/3/movie/{id}"
                response = requests.get(url, headers=headers)
                data = response.json()
                duration = data["runtime"]
                print(f"Popular movie:\nID: {id}, Title: {title}, Rating: {rating} Popularity: {popularity}, Duration: {duration}, Overview: {overview}")
    