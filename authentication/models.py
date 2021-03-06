import re
from string import punctuation, whitespace
from typing import Optional

from places.models import DatePlacesModel, PlaceModel
from pydantic import BaseModel, ValidationError, validator


class RegisterModel(BaseModel):
    fullname: str
    email: str
    phone: str
    password: str
    date: Optional[DatePlacesModel] = None
    places: Optional[list[PlaceModel]] = None
    period: Optional[str] = None
    price: Optional[int] = None

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
        return "7" + phone[1:]

    @validator("password")
    def password_validator(cls, password: str):
        if len(password) < 4:
            raise ValidationError("Password is weak")
        return password


class LoginModel(BaseModel):
    email: str
    password: str


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class UserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    def only_fullname(self):
        return UserModel(fullname=self.fullname)
