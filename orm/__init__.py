import random
import string
import sys
from datetime import datetime, timedelta

from peewee import (
    BooleanField,
    CharField,
    Database,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)


def get_db() -> Database:
    if "pytest" in sys.argv[0].split("\\"):
        return SqliteDatabase(
            "test_database.db",
            pragmas={"journal_mode": "wal", "cache_size": -1024 * 64},
        )
    return SqliteDatabase(
        "database.db", pragmas={"journal_mode": "wal", "cache_size": -1024 * 64}
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


class User(BaseModel):
    full_name = CharField()
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


def create_tables(database: Database = database, base_model: BaseModel = BaseModel):
    with database as db:
        db.create_tables(base_model.__subclasses__())


def drop_tables(database: Database = database, base_model: BaseModel = BaseModel):
    with database as db:
        db.drop_tables(base_model.__subclasses__())
        db.create_tables(base_model.__subclasses__())


if __name__ == "__main__":
    create_tables()
