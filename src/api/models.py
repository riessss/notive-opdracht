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
    func
)
from datetime import datetime, time


# Initialize the db
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


# Deleted year from the database, added rating and popularity
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
    release_date: Mapped[str] = mapped_column(
        nullable=False)
    rating: Mapped[int] = mapped_column(
        nullable=False)
    popularity: Mapped[int] = mapped_column(
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False)


# Deleted endtime this can be calculated with runtime and start_time
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
    start_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False) 
    language: Mapped[str] = mapped_column(
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class Room(db.Model):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(30))
    capacity: Mapped[int] = mapped_column(
        nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    

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
    

# Added genre table
'''class Genre(db.Model):
    __tablename__ = "genres"

    id:
    genre: 
    '''