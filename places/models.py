from datetime import date

from pydantic import BaseModel


class FreePlacesModel(BaseModel):
    start: date
    end: date


class PlaceModel(FreePlacesModel):
    place: int
