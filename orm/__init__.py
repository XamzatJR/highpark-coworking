import sys
from datetime import date, datetime

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
    if sys.argv[0].split("\\")[-1] == "pytest" or (
        len(sys.argv) > 1 and sys.argv[2] == "pytest"
    ):
        return SqliteDatabase(
            "test_database.db",
            pragmas={"journal_mode": "wal", "cache_size": -1024 * 64},
        )
    return SqliteDatabase(
        "database.db", pragmas={"journal_mode": "wal", "cache_size": -1024 * 64}
    )


database = get_db()


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())
    is_active = BooleanField(default=True)

    class Meta:
        database = database

    def save(self, force_insert=False, only=None):
        self.updated_at = datetime.now()
        return super().save(force_insert=force_insert, only=only)


class User(BaseModel):
    full_name = CharField()
    email = CharField(unique=True)
    phone = CharField(unique=True)
    password = CharField()
    is_active = BooleanField(default=False)

    @classmethod
    def get_by_email(cls, email):
        return cls.get_or_none(email=email)


class Place(BaseModel):
    user = ForeignKeyField(User, on_delete="CASCADE")
    place = IntegerField()
    start = DateField(default=date.today())
    end = DateField(default=date.today())


def create_tables(database: Database = database, base_model: BaseModel = BaseModel):
    with database as db:
        db.create_tables(base_model.__subclasses__())


def drop_tables(database: Database = database, base_model: BaseModel = BaseModel):
    with database as db:
        db.drop_tables(base_model.__subclasses__())
        db.create_tables(base_model.__subclasses__())


if __name__ == "__main__":
    create_tables()
