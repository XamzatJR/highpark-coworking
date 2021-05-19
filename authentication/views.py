from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
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
def register(user_model: RegisterModel):
    user_model.password = encrypt_password(user_model.password)
    User.create(**user_model.dict())
    return user_model.exclude_password()


@router.post("/logout")
def logout(request: Request):
    response = JSONResponse()
    response.delete_cookie("Authorization", domain=request.base_url.hostname)
    return response
