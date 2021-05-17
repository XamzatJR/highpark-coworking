from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "uwillneverguess"
    debug: bool = True

    algorithm: str = "sha256_crypt"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def settings() -> Settings:
    return Settings()
