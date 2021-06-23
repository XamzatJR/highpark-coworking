from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

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


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(authentication)
app.include_router(places)
