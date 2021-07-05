import random
import string
from datetime import datetime, timedelta
from typing import Union

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import DATERANGE

from .config import Base, engine


class User(Base):
    __tablename__ = "users"

    fullname = Column(String(55))
    email = Column(String(255), unique=True)
    phone = Column(String(55), unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    code = Column(String, nullable=True)
    expires = Column(DateTime, nullable=True)

    @classmethod
    def create(cls, **kwargs):
        code = "".join(random.choices(string.ascii_letters + string.digits, k=30))
        expires = datetime.now() + timedelta(minutes=10)
        return super().create(code=code, expires=expires, **kwargs)

    @classmethod
    def get_by_email(cls, email: str) -> Union["User", None]:
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def get_by_code(cls, code: str) -> Union["User", None]:
        return cls.query.filter(cls.code == code).first()


class Place(Base):
    __tablename__ = "places"

    user = Column(Integer, ForeignKey(User.id, ondelete="cascade"), primary_key=True)
    place = Column(Integer)
    date = Column(DATERANGE)
    price = Column(Integer, default=0)
    paid_for = Column(Boolean, default=False)


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
