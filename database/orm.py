from datetime import date, datetime

from peewee import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    PrimaryKeyField
)

database = SqliteDatabase(
    "database.db", pragmas={"journal_mode": "wal", "cache_size": -1024 * 64}
)


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
    id = PrimaryKeyField()
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


def create_tables():
    with database:
        database.create_tables(BaseModel.__subclasses__())


create_tables()
