from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime

from .main import db

class Movies(db.Model):
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    external_id: Mapped[int]
    title_nl: Mapped[str] = mapped_column(
        unique=True)
    description_nl: Mapped[str]
    runtime_minutes: Mapped[]

class Screening(db.Model):
    pass

class Room(db.Model):
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(30))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime, nullable=False)
    
class OpeningHour(db.Model):
    id: Mapped[int] = mapped_column(
        primary_key=True)
    day_of_week: Mapped[str] = mapped_column(
        String(15))
    opening_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime, nullable=False)
    closing_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime, nullable=False)
    
class WeekSchedule(db.model):
    id: Mapped[int] = mapped_column(
        primary_key=True)
    week_number:
    year: