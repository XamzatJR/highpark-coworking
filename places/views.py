from orm import Place
from fastapi import APIRouter

from .models import FreePlacesModel, PlaceModel

router = APIRouter(tags=["Places"])


@router.post("/free-places")
def free_places(date_model: FreePlacesModel):
    query = Place.select().where(
        (Place.start <= date_model.start) & (date_model.start <= Place.end)
        | (Place.start <= date_model.end) & (date_model.end <= Place.end)
    )
    places = [
        PlaceModel(place=place.place, start=place.start, end=place.end)
        for place in query
    ]
    return {"places": places}
