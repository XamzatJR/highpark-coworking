from authentication.utils import AuthJWT
from authentication.models import UserModel
from fastapi import APIRouter
from fastapi.params import Depends
from orm import Place

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


@router.get("/profile")
def profile(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_user()
    return UserModel(
        fullname=current_user.fullname,
        email=current_user.email,
        phone=current_user.phone,
    )
