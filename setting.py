from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True

    authjwt_secret_key: str = "uwillneverguess"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    algorithm: str = "sha256_crypt"
    jwt_algorithm: str = "HS256"

    db_name: str = "coworking"
    db_user: str = "postgres"
    db_password: str = "root"
    db_host: str = "127.0.0.1"
    db_port: int = 5432

    email_username: str = ""
    email_from: str = ""
    email_password: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def settings() -> Settings:
    return Settings()
