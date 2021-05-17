from setting import settings

from fastapi import FastAPI

from authentication.views import router as authentication
from places.views import router as places


app = FastAPI(
    debug=settings().debug,
    docs_url="/docs" if settings().debug else "",
    redoc_url="/docs" if settings().debug else "",
)

app.include_router(authentication)
app.include_router(places)
