from fastapi import FastAPI

from authentication.views import router as authentication
from orm import create_tables
from places.views import router as places
from setting import settings

app = FastAPI(
    debug=settings().debug,
    docs_url="/docs" if settings().debug else "",
    redoc_url="/redoc" if settings().debug else "",
)


@app.on_event("startup")
def startup():
    create_tables()


app.include_router(authentication)
app.include_router(places)
