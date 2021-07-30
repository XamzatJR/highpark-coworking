import random
import string
import sys
from datetime import date, datetime, timedelta

from peewee import (
    BooleanField,
    CharField,
    Database,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    PostgresqlDatabase,
    SqliteDatabase,
)

from setting import settings


def get_db() -> Database:
    if "pytest" in sys.argv[0].split("\\"):
        return SqliteDatabase(
            "test_database.db",
            pragmas={"foreign_keys": 1, "cache_size": -1024 * 64},
        )
    return PostgresqlDatabase(
        settings().db_name,
        user=settings().db_user,
        password=settings().db_password,
        host=settings().db_host,
        port=settings().db_port,
    )


database = get_db()


class BaseModel(Model):
    created_at = DateTimeField()
    updated_at = DateTimeField()
    is_active = BooleanField(default=True)

    class Meta:
        database = database

    @classmethod
    def create(cls, **query):
        query["created_at"] = datetime.now()
        query["updated_at"] = datetime.now()
        return super().create(**query)

    def save(self, force_insert=False, only=None):
        self.updated_at = datetime.now()
        return super().save(force_insert=force_insert, only=only)

    def update_by_dict(self, data: dict):
        for key in data:
            setattr(self, key, data[key])
        self.save()


class User(BaseModel):
    fullname = CharField()
    email = CharField(unique=True)
    phone = CharField(unique=True)
    password = CharField()
    is_active = BooleanField(default=False)
    code = CharField(null=True)
    expires = DateTimeField()

    @classmethod
    def create(cls, **query):
        query["code"] = "".join(
            random.choices(string.ascii_letters + string.digits, k=30)
        )
        query["expires"] = datetime.now() + timedelta(minutes=10)
        return super().create(**query)

    @classmethod
    def get_by_email(cls, email: str):
        return cls.get_or_none(email=email)

    @classmethod
    def get_by_code(cls, code: str):
        return cls.get_or_none(code=code, is_active=False)


class Place(BaseModel):
    user = ForeignKeyField(User, on_delete="CASCADE")
    place = IntegerField()
    start = DateField()
    end = DateField()
    price = IntegerField(default=0)
    paid_for = BooleanField(default=False)

    @staticmethod
    def get_places_by_date(date_list: list[date]) -> list["Place"]:
        return Place.select().where(
            (Place.paid_for == True)  # noqa: E712
            & (Place.start.in_(date_list) or Place.end.in_(date_list))
        )


def create_tables(database: Database = database, base_model: BaseModel = BaseModel):
    with database as db:
        db.create_tables(base_model.__subclasses__())


def drop_tables(database: Database = database, base_model: BaseModel = BaseModel):
    with database as db:
        db.drop_tables(base_model.__subclasses__())
        db.create_tables(base_model.__subclasses__())


if __name__ == "__main__":
    create_tables()
