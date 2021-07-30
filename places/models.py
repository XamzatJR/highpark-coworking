from datetime import date
from typing import Optional

from pydantic import BaseModel


class DatePlacesModel(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None


class PlaceModel(BaseModel):
    place: int
    price: Optional[int] = None
    start: Optional[date]
    end: Optional[date]

    class Config:
        orm_mode = True
