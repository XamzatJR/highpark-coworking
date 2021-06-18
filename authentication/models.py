import re
from string import punctuation, whitespace
from typing import Optional

from pydantic import BaseModel, ValidationError, validator


class RegisterModel(BaseModel):
    fullname: str
    email: str
    phone: str
    password: str

    def exclude_password(self):
        model = self
        delattr(model, "password")
        return model

    @validator("email")
    def email_validator(cls, email: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Email not valid")
        return email

    @validator("phone")
    def phone_validator(cls, phone: str):
        for el in punctuation + whitespace:
            phone = phone.replace(el, "")
        if not phone.isdigit():
            raise ValidationError("Phone number not valid")
        if not re.match(r"(8|7)(\d{3})(\d{7})", phone):
            raise ValidationError("Phone number not valid")
        return phone

    @validator("password")
    def password_validator(cls, password: str):
        if len(password) < 5:
            raise ValidationError("Password is weak")
        return password


class LoginModel(BaseModel):
    email: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class UserModel(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
