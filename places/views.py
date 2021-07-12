from datetime import timedelta
from authentication.utils import AuthJWT
from authentication.models import UserModel
from fastapi import APIRouter
from fastapi.params import Depends
from orm.models import Place
from fastapi_sqlalchemy import db
from psycopg2.extras import DateRange


from .models import DatePlacesModel, PlaceModel

router = APIRouter(tags=["Places"])


@router.post("/free-places")
def free_places(dm: DatePlacesModel, Authorize: AuthJWT = Depends()):
    user_places = []

    if dm.start == dm.end:
        dm.end += timedelta(1)

    daterange = DateRange(dm.start - timedelta(1), dm.end + timedelta(1))
    try:
        Authorize.jwt_required()
        user = Authorize.get_user().id
    except Exception:
        user = None
    else:
        user_places = db.session.query(Place).filter(
            Place.date.overlaps(daterange), Place.user == user
        )
    places = db.session.query(Place).filter(
        Place.date.overlaps(daterange), Place.paid_for.is_(True), Place.user != user
    )
    return {
        "places": [PlaceModel.from_orm(obj) for obj in places],
        "user_places": [PlaceModel.from_orm(obj) for obj in user_places],
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
        query = db.session.query(Place).filter(Place.user == user.id, Place.paid_for.is_(False))
        return {"cart": [PlaceModel.from_orm(place) for place in query]}


@router.post("/cart")
def cart_add(place: PlaceModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return {"in_cart": False}


@router.delete("/cart")
def cart_delete(place: PlaceModel, Authorize: AuthJWT = Depends()):
    if place.start is None or place.end is None:
        return {"removed": False}
    id_ = Place.get(**place.dict())
    Place.delete_by_id(id_)
    return {"removed": True}
