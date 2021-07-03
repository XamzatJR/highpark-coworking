from datetime import datetime, timedelta
import random
import string
from typing import Union
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
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
    def get_by_email(cls, email) -> Union["User", None]:
        return cls.query.filter(cls.email == email).first()


class Place(Base):
    __tablename__ = "places"

    user = Column(Integer, ForeignKey(User.id), primary_key=True)
    place = Column(Integer)
    date = Column(DATERANGE())
    price = Column(Integer, default=0)
    paid_for = Column(Boolean, default=False)


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
