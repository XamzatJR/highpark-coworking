from database.orm import Place
from fastapi import APIRouter
from fastapi.param_functions import Depends

from .models import FreePlacesModel, PlaceModel

router = APIRouter(tags=["Places"])


@router.post("/free-places")
def free_places(date_model: FreePlacesModel = Depends()):
    query = Place.select().where(
        (
            Place.start.between(date_model.start, date_model.end)
            or Place.end.between(date_model.start, date_model.end)
        )
    )
    places = [
        PlaceModel(place=place.place, start=place.start, end=place.end)
        for place in query
    ]
    return {"count": len(places), "places": places}
