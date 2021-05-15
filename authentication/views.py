from database.orm import User
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request

from .models import LoginModel, RegisterModel
from .utils import (ACCESS_TOKEN_EXPIRE_MINUTES, check_encrypted_password,
                    create_access_token, encrypt_password)

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(user_model: RegisterModel):
    user_model.password = encrypt_password(user_model.password)
    User.create(**user_model.dict())
    return JSONResponse(status_code=status.HTTP_201_CREATED)


@router.post("/login")
def login(request: Request, user_model: LoginModel):
    user = User.get_by_email(user_model.email)
    http_auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )
    if user is None:
        raise http_auth_error
    if check_encrypted_password(user_model.password, user.password) is False:
        raise http_auth_error
    access_token = create_access_token({"email": user.email})
    response = JSONResponse(None, status.HTTP_200_OK)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        domain=request.base_url.hostname,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return response


@router.post("/logout")
def logout(request: Request):
    response = JSONResponse()
    response.delete_cookie("Authorization", domain=request.base_url.hostname)
    return response
