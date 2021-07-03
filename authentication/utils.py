from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT as _AuthJWT
from orm.models import User
from passlib.context import CryptContext
from setting import settings

ALGORITHM = settings().jwt_algorithm

pwd_context = CryptContext(schemes=[settings().algorithm], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthJWT(_AuthJWT):
    def get_user(self) -> User:
        email = self.get_jwt_subject()
        user = User.get_by_email(email)
        if self._check_user(user):
            return user

    def _check_user(self, user: User):
        http_auth_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"Authenticate": "Bearer"},
        )
        if user is None:
            raise http_auth_error
        if user.is_active is False:
            http_auth_error.detail = "User not active"
            raise http_auth_error
        return True


def encrypt_password(password: str) -> str:
    return pwd_context.hash(password)


def check_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except ValueError:
        return False
