from fastapi.param_functions import Depends
from database.orm import User
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request

from .models import LoginModel, RegisterModel, Token
from .utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    check_password,
    create_access_token,
    encrypt_password,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
def token(user_model: LoginModel = Depends()):
    user = User.get_by_email(user_model.email)
    http_auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"Authenticate": "Bearer"},
    )
    if not user:
        raise http_auth_error
    if (
        check_password(user_model.password, user.password) is False
        or user.is_active is False
    ):
        raise http_auth_error
    access_token = create_access_token({"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
def login(request: Request, user_model: LoginModel = Depends()):
    user = User.get_by_email(user_model.email)
    http_auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"Authenticate": "Bearer"},
    )
    if user is None:
        raise http_auth_error
    if (
        check_password(user_model.password, user.password) is False
        or user.is_active is False
    ):
        raise http_auth_error
    access_token = create_access_token({"email": user.email})
    response = JSONResponse(None, status.HTTP_200_OK)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        domain=request.base_url.hostname,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return response


@router.post("/register")
def register(user_model: RegisterModel = Depends()):
    user_model.password = encrypt_password(user_model.password)
    User.create(**user_model.dict())
    return JSONResponse(status_code=status.HTTP_201_CREATED)


@router.post("/logout")
def logout(request: Request):
    response = JSONResponse()
    response.delete_cookie("Authorization", domain=request.base_url.hostname)
    return response
