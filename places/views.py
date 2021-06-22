from orm import Place
from fastapi import APIRouter

from .models import DatePlacesModel, PlaceModel

router = APIRouter(tags=["Places"])


@router.post("/free-places")
def free_places(date_model: DatePlacesModel):
    query = Place.select().where(
        (Place.paid_for == True)
        & (
            (date_model.start <= Place.start <= date_model.end)
            or (date_model.start <= Place.end <= date_model.end)
        )
    )
    places = [
        PlaceModel(place=place.place, start=place.start, end=place.end)
        for place in query
        if (date_model.start <= place.start <= date_model.end)
        or (date_model.start <= place.end <= date_model.end)
    ]
    return {"places": places}
