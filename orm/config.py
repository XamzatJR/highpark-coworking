from setting import settings
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import DateRange as _DateRange


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
    id = Column(Integer, primary_key=True, autoincrement=True)


class DateRange(_DateRange):
    def to_string(self, *, _format: str = "%Y-%m-%d"):
        return "[{},{})".format(
            self.lower.strftime(_format), self.upper.strftime(_format)
        )
