from places.utils import get_date_range, is_occupied, range_in_range
from authentication.utils import AuthJWT
from authentication.models import UserModel
from fastapi import APIRouter
from fastapi.params import Depends
from orm import Place

from .models import DatePlacesModel, PlaceModel

router = APIRouter(tags=["Places"])


@router.post("/free-places")
def free_places(dm: DatePlacesModel, Authorize: AuthJWT = Depends()):
    places: list[Place]
    user_places: list[Place] = []
    try:
        Authorize.jwt_required()
        user = Authorize.get_user().id
    except Exception:
        user = None
    else:
        user_places = Place.select().where(
            (Place.user == user) & (Place.end >= dm.start)
        )
    places = Place.select().where(
        (Place.paid_for == True)  # noqa: E712
        & (Place.user != user)
        & (Place.end >= dm.start)
    )
    return {
        "places": [
            PlaceModel.from_orm(place)
            for place in places
            if range_in_range(get_date_range(place), [dm.start, dm.end])
        ],
        "user_places": [
            PlaceModel.from_orm(place)
            for place in user_places
            if range_in_range(get_date_range(place), [dm.start, dm.end])
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


@router.get("/cart")
def cart(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        return {"cart": []}
    else:
        user = Authorize.get_user()
        query = Place.select().where(
            (Place.user == user.id) and (Place.paid_for == False)  # noqa: E712
        )
        return {"cart": [PlaceModel.orm(place) for place in query]}


@router.post("/cart/add")
def cart_add(place: PlaceModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user = Authorize.get_user()
    date_list = get_date_range(place)
    places = Place.get_places_by_date(date_list)
    if is_occupied(places, place):
        place = Place.create(user=user, **place.dict())
        return {"in_cart": True}
    return {"in_cart": False}


@router.delete("/cart/detele")
def cart_delete(place: PlaceModel, Authorize: AuthJWT = Depends()):
    if place.start is None or place.end is None:
        return {"removed": False}
    id_ = Place.get(**place.dict())
    Place.delete_by_id(id_)
    return {"removed": True}
