from datetime import datetime, timedelta
from os import environ

from database.orm import User
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = environ.get("SECRET_KEY", "uwillneverguess")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = datetime.now() + timedelta(minutes=60)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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


def encrypt_password(password: str) -> str:
    return pwd_context.encrypt(password)


def check_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except ValueError:
        return False
