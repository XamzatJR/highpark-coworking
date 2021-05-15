from typing import Optional
import re

from pydantic import BaseModel, ValidationError, validator


class RegisterModel(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str

    @validator('full_name')
    def full_name_validator(cls, name):
        if ' ' not in name:
            raise ValidationError('must contain a space')
        return name.title()

    @validator('email')
    def email_validator(cls, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Email not valid")
        return email

    @validator('password')
    def password_validator(cls, password):
        if len(password) < 5:
            raise ValidationError("Password is weak")
        return password


class LoginModel(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
