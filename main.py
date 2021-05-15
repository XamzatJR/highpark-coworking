from os import environ

from fastapi import FastAPI

from authentication.views import router as authentication

DEBUG = bool(environ.get("DEBUG", True))

app = FastAPI(
    debug=DEBUG, docs_url="/docs" if DEBUG else "", redoc_url="/docs" if DEBUG else ""
)

app.include_router(authentication)
