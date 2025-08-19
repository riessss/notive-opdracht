from flask import Blueprint

from models import db, Screening

# Om de helpers te linken met de flask applicatie
bp = Blueprint('auth', __name__, url_prefix='/api/schema')

# Een simpele route die nog niet alle data bevat
# Hiermee kan je wel al het schema zien en controleren dat het werkt
# Het heeft nog wel meer data nodig van de film, deze logica moet ik verbeteren
# in het database schema
@bp.route('/week', methods=["GET"])
def get_week_schedule():
    
    # Haal de bruikbare data op uit de database
    schedules = db.session.query(
        Screening.room_id,
        Screening.movie_id,
        Screening.date,
        Screening.start_time
    ).all()

    # Om de resultaten in JSON te kunnen versturen 
    result = []
    for schedule in schedules:
        result.append({
            "Zaal": schedule.room_id,
            "Begin_tijd": str(schedule.start_time),
            "Film": schedule.movie_id,
            "Datum": schedule.date
        })

    return {"message": result}
