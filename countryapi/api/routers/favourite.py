"""A module containing favourite endpoints."""
from typing import Iterable, Any
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from countryapi.container import Container
from countryapi.core.domain.favourite import Favourite, FavouriteIn, FavouriteBroker
from countryapi.infrastructure.services.ifavourite import IFavouriteService
from countryapi.infrastructure.utils import consts

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", tags=['Favourite'], response_model=Favourite, status_code=201)
@inject
async def create_favourite(
    favourite: FavouriteIn,
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new favourite.

    Args:
        favourite (FavouriteIn): The favourite data.
        service (IFavouriteService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 400 if users favourite already exists.

    Returns:
        dict: The new favourite attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if await get_favourite_by_user(user_uuid):
        raise HTTPException(status_code=400, detail="Your favourite already exists")

    extended_favourite_data = FavouriteBroker(
        user_id=user_uuid,
        **favourite.model_dump(),
    )

    new_favourite = await service.add_favourite(extended_favourite_data)

    return new_favourite.model_dump() if new_favourite else {}

@router.put("/{favourite_id}", tags=['Favourite'], response_model=Favourite, status_code=201)
@inject
async def update_favourite(
    favourite_id: int,
    updated_favourite: FavouriteIn,
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating favourite data.

    Args:
        favourite_id (int): The id of the favourite.
        updated_favourite (FavouriteIn): The updated favourite details.
        service (IFavouriteService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if favourite does not exist.

    Returns:
        dict: The updated favourite details.
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if favourite_data := await service.get_favourite_by_id(favourite_id=favourite_id):
        if str(favourite_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_favourite = FavouriteBroker(
            user_id=user_uuid,
            **updated_favourite.model_dump(),
        )
        new_updated_favourite = await service.update_favourite(
            favourite_id=favourite_id,
            data=extended_updated_favourite,
        )
        return new_updated_favourite.model_dump() if new_updated_favourite \
            else {}

    raise HTTPException(status_code=404, detail="Favourite not found")


@router.delete("/{favourite_id}", tags=['Favourite'], status_code=204)
@inject
async def delete_favourite(
    favourite_id: int,
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting favourite.

    Args:
        favourite_id (int): The id of the favourite.
        service (IFavouriteService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if favourite does not exist.

    Returns:
        dict: Empty if operation finished.
    """
    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if favourite_data := await service.get_favourite_by_id(favourite_id=favourite_id):
        if str(favourite_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")
        await service.delete_favourite(favourite_id)
        return

    raise HTTPException(status_code=404, detail="Favourite not found")


@router.get("/{favourite_id}", tags=['Favourite'], response_model=Favourite, status_code=200)
@inject
async def get_favourite_by_id(
    favourite_id: int,
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
) -> dict:
    """An endpoint for getting favourite details by id.

    Args:
        favourite_id (int): The id of the favourite.
        service (IFavouriteService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if favourite does not exist.

    Returns:
        dict: The requested favourite attributes.
    """
    if favourite := await service.get_favourite_by_id(favourite_id):
        return favourite.model_dump()

    raise HTTPException(status_code=404, detail="Favourite not found")

@router.get("/all/{all}", tags=['Favourite'], response_model=Iterable[Favourite], status_code=200)
@inject
async def get_all_favourites(
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
) -> Iterable:
    """An endpoint for getting all favourites.

    Args:
        service (IFavouriteService, optional): The injected service dependency.

    Returns:
        Iterable: The favourites attributes collection.
    """
    favourites = await service.get_all_favourites()

    return favourites


@router.get("/ranking/{ranking}", tags=['Favourite'], response_model=Any, status_code=200)
@inject
async def get_ranking(
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
) -> Iterable:
    """An endpoint for getting favourites ranking.

    Args:
        service (IFavouriteService, optional): The injected service dependency.

    Returns:
        Iterable: The favourite countries ranking.
    """
    ranking = await service.get_ranking()

    return ranking

@router.get("/country/{country_name}", tags=['Favourite'], response_model=Iterable[Favourite], status_code=200)

@inject
async def get_favourite_by_country(
    country_name: str,
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
) -> Iterable:
    """An endpoint for getting favourite details by country name.

    Args:
        country_name (str): The name of the country.
        service (IFavouriteService, optional): The injected service dependency.

    Returns:
        Iterable: The favourites attributes collection.
    """
    favourite = await service.get_favourite_by_country(country_name)

    return favourite


@router.get("/user/{user_id}", tags=['Favourite'], response_model=Iterable[Favourite], status_code=200)

@inject
async def get_favourite_by_user(
    user_id: UUID4,
    service: IFavouriteService = Depends(Provide[Container.favourite_service]),
) -> Iterable:
    """An endpoint for getting favourite details by user id.

    Args:
        user_id (UUID4): The id of the user.
        service (IFavouriteService, optional): The injected service dependency.

    Returns:
        Iterable: The favourites attributes collection.
    """
    favourite = await service.get_favourite_by_user(user_id)

    return favourite

