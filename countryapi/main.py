"""Main module of the app"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from countryapi.api.routers.country import router as country_router
from countryapi.api.routers.continent import router as continent_router
from countryapi.api.routers.visited import router as visited_router
from countryapi.api.routers.favourite import router as favourite_router
from countryapi.api.routers.user import router as user_router
from countryapi.container import Container
from countryapi.db import database
from countryapi.db import init_db


container = Container()
container.wire(modules=[
    "countryapi.api.routers.continent",
    "countryapi.api.routers.user",
    "countryapi.api.routers.country",
    "countryapi.api.routers.visited",
    "countryapi.api.routers.favourite",

])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(country_router, prefix="/country")
app.include_router(continent_router, prefix="/continent")
app.include_router(visited_router, prefix="/visited")
app.include_router(favourite_router, prefix="/favourite")

app.include_router(user_router, prefix="")



@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
