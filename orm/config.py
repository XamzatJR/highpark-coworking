from setting import settings
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query

DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    settings().db_user,
    settings().db_password,
    settings().db_host,
    settings().db_port,
    settings().db_name,
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @classmethod
    def create(cls, **kwargs):
        with Session() as session:
            obj = cls(**kwargs)
            session.add(obj)
            session.commit()
        return obj

    @classmethod
    @property
    def query(cls) -> Query:
        with Session() as session:
            return session.query(cls)
