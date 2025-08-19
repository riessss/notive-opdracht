from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    DeclarativeBase
)
from sqlalchemy import (
    String,
    DateTime, 
    ForeignKey, 
    Time, 
    Date,
    func
)

# Created_at en updated_at heb ik elke tabel automatisch laten toeveogen
# Hetzelfde voor autoincrement
# De relationships heb ik weergegeven met de ForeignKey

# Gekozen voor date time om zo betere leesbaarheid te hebben in de code
from datetime import datetime, time, date


# De database setup, gekozen om het hier te doen vanwege de snelheid
# In een grotere codebase kan dit beter ergens anders
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


# Ik heb hier alleen release date en geen jaar in de tabel
# Dit is dubbele data dus is niet nodig, hierdoor had ik ook extra
# bewerkingen moeten maken aan de data vanuit de api
# Rating en populariteit toegevoegd
class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    external_id: Mapped[int] = mapped_column(
        nullable=False, unique=True)
    title_nl: Mapped[str]
    description_nl: Mapped[str] = mapped_column(
        nullable=False)
    runtime_minutes: Mapped[int] = mapped_column(
        nullable=False)
    release_date: Mapped[date] = mapped_column(
        Date, nullable=False)
    rating: Mapped[int] = mapped_column(
        nullable=True)
    popularity: Mapped[int] = mapped_column(
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False)


# Deze tabel is gelijk gebleven met het voorbeeld
# De logica van het koppelen met het week_schedule is niet helemaal gelukt
# Daarnaast om queries makkelijker te maken had ik hier relationships aan toe kunnen voegen
# Dit zou nog handig zijn als om de API te verbeteren
class Screening(db.Model):
    __tablename__ = "screenings"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    week_schedule_id: Mapped[int] = mapped_column(
        ForeignKey("week_schedules.id"))
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"))
    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"))
    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False)
    start_time: Mapped[time] = mapped_column(
        Time, nullable=False) 
    language: Mapped[str] = mapped_column(
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False)

# De zelfde data als in de tabel
class Room(db.Model):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(30), nullable=False)
    capacity: Mapped[int] = mapped_column(
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
# Dezelde data als de tabel, opnieuw gekozen voor tijd en inplaats van string
class OpeningHour(db.Model):
    __tablename__ = "opening_hours"

    id: Mapped[int] = mapped_column(
        primary_key=True)
    day_of_week: Mapped[str] = mapped_column(
        String(15))
    opening_time: Mapped[time] = mapped_column(
        Time, nullable=False)
    closing_time: Mapped[time] = mapped_column(
        Time, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    
# Hetzelfde gehouden als het schema
# Deze tabel heb ik niet optimaal kunnen gebruiken en loopt niet gelijk met de date
# van de screening tabel. Dit moet verbeterd worken, anders is deze tabel niet echt
# van toegevoegde waarde.
class WeekSchedule(db.Model):
    __tablename__ = "week_schedules"

    id: Mapped[int] = mapped_column(
        primary_key=True)
    week_number: Mapped[int] = mapped_column(
        nullable=False)
    year: Mapped[int] = mapped_column(
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
