from models import (
    Room, 
    OpeningHour, 
    WeekSchedule,
    db
)
from datetime import time

# De zalen zijn statische data, daarom kiezs ik er voor om deze vooraf toe te voegen
# Ik heb de capacitiet met 50 ingevuld omdat ik zodat notive er bijna twee keer in past
def add_rooms():
    if not Room.query.first():
        room1 = Room(name="Zaal 1", capacity=50)
        room2 = Room(name="Zaal 2", capacity=50)
        
        db.session.add_all([room1, room2])
        db.session.commit()


# Hetzelfde geld voor de openings tijden, deze heb ik ook vooraf toegevoegd
# Ik heb gekozen voor time om zo beter te kunnen rekenen met de minuten
def add_openhours():
    if not OpeningHour.query.first():
        monday = OpeningHour(
            day_of_week="Maandag", 
            opening_time=time(10, 0),
            closing_time=time(20, 0))
        tuesday = OpeningHour(
            day_of_week="Dinsdag", 
            opening_time=time(8, 0),
            closing_time=time(21, 0))
        wednesday = OpeningHour(
            day_of_week="Woensdag", 
            opening_time=time(8, 0),
            closing_time=time(21, 0))
        thursday = OpeningHour(
            day_of_week="Donderdag", 
            opening_time=time(8, 0),
            closing_time=time(21, 0))
        friday = OpeningHour(
            day_of_week="Vrijdag", 
            opening_time=time(8, 0),
            closing_time=time(0, 0))
        saturday = OpeningHour(
            day_of_week="Zaterdag", 
            opening_time=time(10, 0),
            closing_time=time(0, 0))
        sunday = OpeningHour(
            day_of_week="Zondag", 
            opening_time=time(10, 0),
            closing_time=time(22, 0))
        
        db.session.add_all([
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday
        ])
        db.session.commit()
    
# Ik heb deze tabel statisch gemaakt om compleziteit te voorkomen
# De id's zijn nu op auto increment, ik had dit kunnen gelijk stellen met
# de datum van de dag dat de code online wordt gezet, dit voegt wel
# extra compleziteit toe. 
# Deze data/tabel heeft me uiteindelijk veel denkwerk opgeleverd en ben ik 
# mischien iets te lang bij blijven hangen
def add_week_schedule():
    for year in range(2025, 2028):
        for week in range(0, 52):
            week_number = week + 1

            week_schedule = WeekSchedule(
                week_number=week_number, 
                year=year)
            db.session.add(week_schedule)
            db.session.commit()
    