"""A module containing visited endpoints."""
from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from countryapi.container import Container
from countryapi.core.domain.visited import Visited, VisitedIn, VisitedBroker
from countryapi.infrastructure.services.ivisited import IVisitedService
from countryapi.infrastructure.utils import consts

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.post("/create", response_model=Visited, status_code=201)
@inject
async def create_visited(
    visited: VisitedIn,
    service: IVisitedService = Depends(Provide[Container.visited_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new visited.

    Args:
        visited (VisitedIn): The visited data.
        service (IVisitedService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The new visited attributes.
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

    extended_visited_data = VisitedBroker(
        user_id=user_uuid,
        **visited.model_dump(),
    )

    new_visited = await service.add_visited(extended_visited_data)

    return new_visited.model_dump() if new_visited else {}

@router.put("/{visited_id}", response_model=Visited, status_code=201)
@inject
async def update_visited(
    visited_id: int,
    updated_visited: VisitedIn,
    service: IVisitedService = Depends(Provide[Container.visited_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating visited data.

    Args:
        visited_id (int): The id of the visited.
        updated_visited (VisitedIn): The updated visited details.
        service (IVisitedService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if visited does not exist.

    Returns:
        dict: The updated visited details.
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

    if visited_data := await service.get_visited_by_id(visited_id=visited_id):
        if str(visited_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_visited = VisitedBroker(
            user_id=user_uuid,
            **updated_visited.model_dump(),
        )
        new_updated_visited = await service.update_visited(
            visited_id=visited_id,
            data=extended_updated_visited,
        )
        return new_updated_visited.model_dump() if new_updated_visited \
            else {}

    raise HTTPException(status_code=404, detail="Visited not found")


@router.delete("/{visited_id}", status_code=204)
@inject
async def delete_visited(
    visited_id: int,
    service: IVisitedService = Depends(Provide[Container.visited_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting visited.

    Args:
        visited_id (int): The id of the visited.
        service (IVisitedService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if visited does not exist.

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

    if visited_data := await service.get_visited_by_id(visited_id=visited_id):
        if str(visited_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")
        await service.delete_visited(visited_id)
        return

    raise HTTPException(status_code=404, detail="Visited not found")


@router.get("/{visited_id}", response_model=Visited, status_code=200)
@inject
async def get_visited_by_id(
    visited_id: int,
    service: IVisitedService = Depends(Provide[Container.visited_service]),
) -> dict:
    """An endpoint for getting visited details by id.

    Args:
        visited_id (int): The id of the visited.
        service (IVisitedService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if visited does not exist.

    Returns:
        dict: The requested visited attributes.
    """
    if visited := await service.get_visited_by_id(visited_id):
        return visited.model_dump()

    raise HTTPException(status_code=404, detail="Visited not found")

@router.get("/all/{all}", response_model=Iterable[Visited], status_code=200)
@inject
async def get_all_visited(
    service: IVisitedService = Depends(Provide[Container.visited_service]),
) -> Iterable:
    """An endpoint for getting all visited.

    Args:
        service (IVisitedService, optional): The injected service dependency.

    Returns:
        Iterable: The visited attributes collection.
    """
    visited = await service.get_all_visited()

    return visited



@router.get("/country/{country_name}", response_model=Iterable[Visited], status_code=200)

@inject
async def get_visited_by_country(
    country_name: str,
    service: IVisitedService = Depends(Provide[Container.visited_service]),
) -> Iterable:
    """An endpoint for getting visited details by country name.

    Args:
        country_name (str): The name of the country.
        service (IVisitedService, optional): The injected service dependency.

    Returns:
        Iterable: The visited attributes collection.
    """
    visited = await service.get_visited_by_country(country_name)

    return visited


@router.get("/user/{user_id}", response_model=Iterable[Visited], status_code=200)

@inject
async def get_visited_by_user(
    user_id: UUID4,
    service: IVisitedService = Depends(Provide[Container.visited_service]),
) -> Iterable:
    """An endpoint for getting visited details by user id.

    Args:
        user_id (UUID4): The id of the user.
        service (IVisitedService, optional): The injected service dependency.

    Returns:
        Iterable: The visited attributes collection.
    """
    visited = await service.get_visited_by_user(user_id)

    return visited

