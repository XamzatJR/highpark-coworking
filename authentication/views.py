from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import JSONResponse
from mail import send_activation
from orm import User
from starlette.requests import Request

from .models import LoginModel, RegisterModel, TokenModel
from .utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    check_user,
    create_access_token,
    encrypt_password,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenModel)
def token(user_model: LoginModel):
    user = User.get_by_email(user_model.email)
    check_user(user_model, user)
    access_token = create_access_token({"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
def login(request: Request, user_model: LoginModel):
    user = User.get_by_email(user_model.email)
    check_user(user_model, user)
    access_token = create_access_token({"email": user.email})
    response = JSONResponse(
        None, status.HTTP_200_OK, {"Authorization": f"Bearer {access_token}"}
    )
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        domain=request.base_url.hostname,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return response


@router.post("/register")
def register(
    request: Request, user_model: RegisterModel, background_tasks: BackgroundTasks
):
    user_model.password = encrypt_password(user_model.password)
    user = User.create(**user_model.dict())
    background_tasks.add_task(send_activation, request.base_url._url, user)
    return user_model.exclude_password()


@router.get("/activate/")
def activate_user(code: str):
    user = User.get_by_code(code)
    if not user:
        return {"error": "Сan't find the user"}
    if datetime.now() > user.expires:
        return {"error": "Сode expired"}
    user.is_active = True
    user.code = None
    user.save()
    return {"message": "User has been activated"}


@router.post("/logout")
def logout(request: Request):
    response = JSONResponse()
    response.delete_cookie("Authorization", domain=request.base_url.hostname)
    return response
