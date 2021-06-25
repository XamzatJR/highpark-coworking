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
        (Place.paid_for == True)  # noqa: E712
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

    user = Authorize.get_user()
    return UserModel(
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
    )


@router.patch("/profile")
def profile_update(data: UserModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    data = data.dict(exclude_unset=True)
    user = Authorize.get_user().update_by_dict()
    access_token = Authorize.create_access_token(
        subject=user.email, expires_time=(60 * 60 * 24)
    )
    Authorize.set_access_cookies(access_token, max_age=(60 * 60 * 24))
    return UserModel(
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
    )
