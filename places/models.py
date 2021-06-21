from datetime import date
from typing import Optional

from pydantic import BaseModel


class DatePlacesModel(BaseModel):
    start: date
    end: date


class PlaceModel(BaseModel):
    place: int
    start: Optional[date]
    end: Optional[date]
