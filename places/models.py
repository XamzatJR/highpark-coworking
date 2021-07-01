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

    @classmethod
    def orm(cls, model):
        return cls(
            place=model.place, price=model.price, start=model.start, end=model.end
        )
