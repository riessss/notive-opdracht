from models import (
    Movie,
    Screening,
    OpeningHour,
    WeekSchedule,
    db
)
from datetime import datetime, timedelta, date
import time

# Ik heb er voor gekozen om de film van laat naar vroeg in te delen omdat de meeste mensen 
# in de avond naar de film gaan

# Hier kan meer error handling worden toegevoegd, en meer logica worden getest 

# De twee zalen opgedeeld in twee functies om zo de verschillende films in te kunnen delen
def create_schedule_hall1():

    # Om te wachten tot dat de films ingeladen zijn om zo fouten te voorkomen
    time.sleep(120)

    # De populaire films voor deze zaal
    movies = Movie.query.filter(Movie.rating > 8).all()
    movie_used_id = 0

    # Hier voor gekozen om het per id te doen
    # Dit loopt niet gelijk met het jaar, niet accurate dus
    week_schedule = WeekSchedule.query.order_by(WeekSchedule.id.desc()).first()
    week_schedule_id = week_schedule.id

    # Maak per week een schema voor 10 weken, dit kan meer zijn op basis van de behoefte
    # Dit is een nadeel van een thread. De code kan niet oneindig runnen en op afstand bestuurd worden
    for week in range(0, 10):
        
        # Per dag de films indelen die hierboven zijn opgehaald
        for day in range(1, 8):
            # De openingstijd ophalen om zo de tijden van de film te kunnen berekenen
            week_day = OpeningHour.query.filter_by(id=day).first()
        
            # De openings tijden naar datetime veranderd om zo de minuten te kunnen berekenen
            opening_dt = datetime.combine(datetime.today(), week_day.opening_time)
            closing_dt = datetime.combine(datetime.today(), week_day.closing_time)
            minutes_open = (closing_dt - opening_dt).total_seconds() / 60
        
            # Gebruikt om voor elke film een nieuwe berekening te maken voor de begin tijd
            current_end = closing_dt  

            # Om te zorgen dat de loop stopt als de dag vol is met films
            time_left = True
            # Dit kan verbeterd worden door opnieuw door de films heen te gaan als de laatste 
            # film is ingedeeld
            while time_left and movie_used_id < len(movies):

                # Om de film niet in te delen en naar de volgende dag te gaan als er niet genoeg tijd is
                runtime = movies[movie_used_id].runtime_minutes              
                if minutes_open < runtime:
                    time_left = False
                    break
        
                # Bereken de start tijd en zorg dat dit op de 5 minuten is om het uniform te houden
                start_dt = current_end - timedelta(minutes=runtime)
                start_dt = start_dt.replace(minute=(start_dt.minute // 5) * 5,
                                second=0, microsecond=0)            
    
                # De start tijd omgerekend naar tijd om aan de database te kunnen worden toegevoegd
                start_time = start_dt.time()
    
                # De datum van elke maandag berekend om elke schema vanaf maandag te laten lopen
                # Dit zorgt er voor dat de dag goed loopt met de datum
                today = date.today()
                this_week_monday = today - timedelta(days=today.weekday())
                movie_date = this_week_monday + timedelta(days=7 + day)
        
                # Data in de database gestopt, hier 
                screening = Screening(
                    week_schedule_id=(week_schedule_id + week),
                    # Voor zaal 1
                    room_id=1,
                    movie_id=movies[movie_used_id].id,
                    date=movie_date,
                    start_time=start_time,
                    language="Nederlands"
                )
                db.session.add(screening)
                db.session.commit()
                print("movie scheduled")
        
                # Update de huidige tijden om zo de berekeningen het kunnen maken voor de volgende film
                current_end = start_dt - timedelta(minutes=15)  # 15 minuten pauze
                minutes_open -= (runtime + 15)
        
                # Doe hetzelfde voor de volgende film
                movie_used_id += 1
    
        # Doe hetzelde process na een week
        time.sleep(60*60*24*7)

# Hetzelfde als de vorig functie alleen wordt hier gefilterd op data
def create_schedule_hall2():
    time.sleep(120)

    # Filter op datum
    movies = Movie.query.filter(Movie.release_date > date(1995, 1, 1)).all()
    movie_used_id = 0

    week_schedule = WeekSchedule.query.order_by(WeekSchedule.id.desc()).first()
    week_schedule_id = week_schedule.id

    for week in range(0, 10):
        
        for day in range(1, 8):
            week_day = OpeningHour.query.filter_by(id=day).first()
        
            opening_dt = datetime.combine(datetime.today(), week_day.opening_time)
            closing_dt = datetime.combine(datetime.today(), week_day.closing_time)
            
            minutes_open = (closing_dt - opening_dt).total_seconds() / 60
        
            current_end = closing_dt 
            time_left = True
        
            while time_left and movie_used_id < len(movies):
                runtime = movies[movie_used_id].runtime_minutes               
        
                if minutes_open < runtime:
                    time_left = False
                    break
        
                start_dt = current_end - timedelta(minutes=runtime)
                start_dt = start_dt.replace(minute=(start_dt.minute // 5) * 5,
                                second=0, microsecond=0)            
    
                start_time = start_dt.time()
    
                today = date.today()
    
                this_week_monday = today - timedelta(days=today.weekday())
    
                movie_date = this_week_monday + timedelta(days=7 + day)
        
                screening = Screening(
                    week_schedule_id=(week_schedule_id + week),
                    # Voor zaal 2
                    room_id=2,
                    movie_id=movies[movie_used_id].id,
                    date=movie_date,
                    start_time=start_time,
                    language="Nederlands"
                )
                db.session.add(screening)
                db.session.commit()
                print("movie scheduled")
        
                current_end = start_dt - timedelta(minutes=15)
                minutes_open -= (runtime + 15)
        
                movie_used_id += 1
    
        time.sleep(60*60*24*7)