from datetime import timedelta
from orm import Place
from places.models import PlaceModel


def get_date_range(date):
    days = (date.end - date.start).days + 2
    return [date.start + timedelta(days=x - 1) for x in range(days)]


def is_occupied(places: list[Place], place: PlaceModel) -> bool:
    for plc in places:
        if (plc.place == place.place) and (
            plc.start == place.start or plc.end == place.end
        ):
            return True
    return False
