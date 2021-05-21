from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True

    secret_key: str = "uwillneverguess"
    algorithm: str = "sha256_crypt"
    jwt_algorithm: str = "HS256"

    email_username: str
    email_from: str
    email_password: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def settings() -> Settings:
    return Settings()
