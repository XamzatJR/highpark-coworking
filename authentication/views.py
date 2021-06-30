from datetime import datetime
from places.utils import get_date_range, is_occupied

from fastapi.exceptions import HTTPException
from setting import settings

from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.responses import JSONResponse
from mail import send_activation
from orm import Place, User

from .models import LoginModel, RegisterModel, TokenModel
from .utils import check_password, encrypt_password, AuthJWT

router = APIRouter(prefix="/auth", tags=["Auth"])


@AuthJWT.load_config
def get_config():
    return settings()


@router.post("/token", response_model=TokenModel)
def token(user_model: LoginModel, Authorize: AuthJWT = Depends()):
    user = User.get_by_email(user_model.email)
    if not user or not check_password(user_model.password, user.password):
        http_auth_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"Authenticate": "Bearer"},
        )
        raise http_auth_error
    access_token = Authorize.create_access_token(
        subject=user.email, expires_time=(60 * 60 * 24)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
def login(request: Request, user_model: LoginModel, Authorize: AuthJWT = Depends()):
    user = User.get_by_email(user_model.email)
    if not user or not check_password(user_model.password, user.password):
        http_auth_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"Authenticate": "Bearer"},
        )
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
    user = User.create(**user_model.dict())
    background_tasks.add_task(send_activation, request.base_url._url, user)
    if user_model.date and user_model.places:
        date_list = get_date_range(user_model.date)
        places = Place.select().where(
            (Place.paid_for == True)  # noqa: E712
            & (Place.start.in_(date_list) or Place.end.in_(date_list))
        )
        for place in user_model.places:
            if is_occupied(places, place):
                continue
            Place.create(
                user=user,
                place=place.place,
                start=user_model.date.start,
                end=user_model.date.end,
                price=user_model.price
                * (
                    len(date_list)
                    if user_model.period == "day"
                    else len(date_list) // 30
                ),
            )
    return user_model.exclude_password()


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
