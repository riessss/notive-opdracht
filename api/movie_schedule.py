from celery import Celery, Task
import requests

page = 1

url = f"https://api.themoviedb.org/3/movie/popular?language=nl-US&page={page}"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNWFiNDQyN2RiYThhMmE4OWFhZjA3MDQ1ZDQzOWEzOCIsIm5iZiI6MTc1NTU0NDcwNC42NzIsInN1YiI6IjY4YTM3YzgwOWJmNTMyMDc0NDgzYjZiMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XDbXSupzUUplvXY3nV3Oc84uSCkzhxysok92DL6KStA"
}

response = requests.get(url, headers=headers)

result = response.json()

movies = result["results"]

for movie in result["results"]:
    id = movie["id"]
    title = movie["title"]
    overview = movie["overview"]
    if id and title and overview: 
        print(f"ID: {id}, Title: {title}, Overview: {overview}")