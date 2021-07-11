import itertools
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
from mail import send_activation
from orm.models import Place, User
from psycopg2.extras import DateRange
from setting import settings

from .models import LoginModel, RegisterModel, TokenModel
from .utils import AuthJWT, check_password, encrypt_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@AuthJWT.load_config
def get_config():
    return settings()


@router.post("/token", response_model=TokenModel)
def token(user_model: LoginModel, Authorize: AuthJWT = Depends()):
    user = User.get_by_email(user_model.email)

    http_auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"Authenticate": "Bearer"},
    )

    if not user or not check_password(user_model.password, user.password):
        raise http_auth_error
    if user.is_active is False:
        http_auth_error.detail = "User not active"
        raise http_auth_error

    access_token = Authorize.create_access_token(
        subject=user.email, expires_time=(60 * 60 * 24)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
def login(user_model: LoginModel, Authorize: AuthJWT = Depends()):
    user = User.get_by_email(user_model.email)

    http_auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"Authenticate": "Bearer"},
    )

    if not user or not check_password(user_model.password, user.password):
        raise http_auth_error
    if user.is_active is False:
        http_auth_error.detail = "User not active"
        raise http_auth_error

    access_token = Authorize.create_access_token(
        subject=user.email, expires_time=(60 * 60 * 24)
    )
    Authorize.set_access_cookies(access_token, max_age=(60 * 60 * 24))
    return {"msg": "Successfully login"}


@router.post("/register")
def register(
    request: Request, user_model: RegisterModel, background_tasks: BackgroundTasks
):
    user_model.password = encrypt_password(user_model.password)

    try:
        user = User.create(
            **user_model.dict(exclude={"date", "places", "period", "price"})
        )
    except Exception as err:
        err_msg = err.orig.pgerror
        if "users_phone_key" in err_msg:
            return {"error": "phone"}
        return {"error": "email"}

    db.session.add(user)
    db.session.commit()

    background_tasks.add_task(send_activation, request.base_url._url, user)

    if not user_model.date or not user_model.places:
        return user_model.dict(
            exclude={"password", "date", "places", "period", "price"}
        )

    daterange = DateRange(user_model.date.start, user_model.date.end)
    places = db.session.query(Place).filter(
        ~Place.date.in_([daterange]), Place.paid_for.is_(True)
    ).values(Place.place)
    if places is None:
        places = []
    places = list(itertools.chain(*places))
    days = (user_model.date.end - user_model.date.start).days
    if user_model.period == "month":
        days = days // 30
    for place in user_model.places:
        if place.place in places:
            continue
        place = Place(
            user=user.id,
            place=place.place,
            date=daterange,
            price=user_model.price * days
        )
        db.session.add(place)
        db.session.commit()
    return user_model.dict(exclude={"password", "date", "places", "period", "price"})


@router.get("/activate")
def activate_user(code: str):
    user = User.get_by_code(code)

    if not user:
        return JSONResponse(
            {"error": "Сan't find the user"}, status.HTTP_204_NO_CONTENT
        )
    if datetime.now() > user.expires:
        return JSONResponse({"error": "Сode expired"}, status.HTTP_204_NO_CONTENT)

    user.is_active = True
    user.expires = None
    user.code = None
    user.save()
    return JSONResponse({"message": "User has been activated"}, status.HTTP_200_OK)


@router.post("/logout")
def logout(Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


@router.post("/verify")
def verify(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        return {"valid": False}
    else:
        return {"valid": True}
