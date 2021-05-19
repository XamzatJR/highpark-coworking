from datetime import datetime, timedelta

from orm import User
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from setting import settings

from .models import LoginModel

SECRET_KEY = settings().secret_key
ALGORITHM = settings().jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = datetime.now() + timedelta(minutes=60)

pwd_context = CryptContext(schemes=[settings().algorithm], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def oauth2_get_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email", None)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = User.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def get_current_user(current_user: User = Depends(oauth2_get_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def check_user(user_model: LoginModel, user: User):
    http_auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"Authenticate": "Bearer"},
    )
    if user is None:
        raise http_auth_error
    if check_password(user_model.password, user.password) is False:
        raise http_auth_error
    if user.is_active is False:
        http_auth_error.detail = "User not active"
        raise http_auth_error


def encrypt_password(password: str) -> str:
    return pwd_context.hash(password)


def check_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except ValueError:
        return False
