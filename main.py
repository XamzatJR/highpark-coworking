from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from authentication.views import router as authentication
from orm import create_tables
from places.views import router as places
from setting import settings

app = FastAPI(
    debug=settings().debug,
    docs_url="/docs" if settings().debug else "",
    redoc_url="/redoc" if settings().debug else "",
)


if settings().debug:
    origins = [
        "http://127.0.0.1",
        "http://127.0.0.1:5500",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def startup():
    create_tables()


app.include_router(authentication)
app.include_router(places)
