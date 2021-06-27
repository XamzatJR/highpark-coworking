from datetime import timedelta
from authentication.utils import AuthJWT
from authentication.models import UserModel
from fastapi import APIRouter
from fastapi.params import Depends
from orm import Place

from .models import DatePlacesModel, PlaceModel

router = APIRouter(tags=["Places"])


@router.post("/free-places")
def free_places(date_model: DatePlacesModel, Authorize: AuthJWT = Depends()):
    places: list[Place]
    user_places: list[Place] = []

    days = (date_model.end - date_model.start).days + 2
    date_model.start -= timedelta(1)
    date_list = [date_model.start + timedelta(days=x) for x in range(days)]
    date_condition = Place.start.in_(date_list) or Place.end.in_(date_list)
    try:
        Authorize.jwt_required()
        user = Authorize.get_user().id
    except Exception:
        user = None
    else:
        user_places = Place.select().where((Place.user == user) & date_condition)
    places = Place.select().where(
        (Place.paid_for == True) & (Place.user != user) & date_condition  # noqa: E712
    )
    return {
        "places": [PlaceModel.orm(place) for place in places if date_condition],
        "paid_for": [
            PlaceModel.orm(place) for place in user_places if place.paid_for is True
        ],
        "not_paid_for": [
            PlaceModel.orm(place) for place in user_places if place.paid_for is False
        ],
    }


@router.get("/profile")
def profile(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    user = Authorize.get_user()
    return UserModel(
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
    )


@router.patch("/profile")
def profile_update(data: UserModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    data = data.only_fullname().dict(exclude_unset=True)
    Authorize.get_user().update_by_dict(data)
    return data
