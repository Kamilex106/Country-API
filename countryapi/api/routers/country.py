"""A module containing country endpoints."""
from typing import Iterable, Any
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from countryapi.infrastructure.utils import consts
from countryapi.container import Container
from countryapi.core.domain.country import Country, CountryIn, CountryBroker
from countryapi.infrastructure.dto.countrydto import CountryDTO
from countryapi.infrastructure.services.icountry import ICountryService


bearer_scheme = HTTPBearer()
router = APIRouter()


@router.post("/create", tags=['Country'], response_model=Country, status_code=201)
@inject
async def create_country(
    country: CountryIn,
    service: ICountryService = Depends(Provide[Container.country_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new country.

    Args:
        country (CountryIn): The country data.
        service (ICountryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if country already exist.
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if continent does not exist.

    Returns:
        dict: The new country attributes.
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


    extended_country_data = CountryBroker(
        user_id=user_uuid,
        **country.model_dump(),
    )
    if await service.get_by_name(extended_country_data.name) is not None:
        raise HTTPException(
            status_code=400,
            detail="Country already exist",
        )

    if new_country := await service.add_country(extended_country_data):
        return new_country.model_dump()

    raise HTTPException(
        status_code=404,
        detail="Continent not exist",
    )



@router.put("/{country_id}", tags=['Country'], response_model=Country, status_code=201)
@inject
async def update_country(
    country_id: int,
    updated_country: CountryIn,
    service: ICountryService = Depends(Provide[Container.country_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating country data.

    Args:
        country_id (int): The id of the country.
        updated_country (CountryIn): The updated country details.
        service (ICountryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if continent does not exist.
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if country does not exist.

    Returns:
        dict: The updated country details.
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

    if country_data := await service.get_by_id(country_id=country_id):
        if str(country_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_country = CountryBroker(
            user_id=user_uuid,
            **updated_country.model_dump(),
        )
        if updated_country_data := await service.update_country(
            country_id=country_id,
            data=extended_updated_country,
        ):
            return updated_country_data.model_dump()
        else:
            raise HTTPException(status_code=400, detail="Continent not exist")

    raise HTTPException(status_code=404, detail="Country not found")



@router.delete("/{country_id}", tags=['Country'], status_code=204)
@inject
async def delete_country(
    country_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> None:
    """An endpoint for deleting country.

    Args:
        country_id (int): The id of the country.
        service (ICountryService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if country does not exist.

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

    if country_data := await service.get_by_id(country_id=country_id):
        if str(country_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")
        await service.delete_country(country_id)
        return

    raise HTTPException(status_code=404, detail="Country not found")



@router.get("/all", tags=['Country'], response_model=Iterable[CountryDTO], status_code=200)
@inject
async def get_all_countries(
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting all countries.

    Args:
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """

    countries = await service.get_all()

    return countries

@router.get(
        "/continent/summary/by",
        tags=['Country'],
        response_model=Any,
        status_code=200,
)
@inject
async def get_summary_by_continent(
    continent_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries summary by continent.

    Args:
        continent_id (int): The continent id.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries in continent summary by PKB, area and inhabitants.
    """
    countries = await service.get_summary_by_continent(continent_id)

    return countries

@router.get(
        "/continent/summary/all",
        tags=['Country'],
        response_model=Any,
        status_code=200,
)
@inject
async def get_summary_by_all_continents(
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries summary by all continents.

    Args:
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries in all continents summary by PKB, area and inhabitants.
    """
    countries = await service.get_summary_by_all_continents()

    return countries



@router.get(
        "/continent/{continent_id}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def get_countries_by_continent(
    continent_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries by continent.

    Args:
        continent_id (int): The continent id.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.get_by_continent(continent_id)

    return countries


@router.get(
        "/{country_id}",
        tags=['Country'],
        response_model=CountryDTO,
        status_code=200,
)
@inject
async def get_country_by_id(
    country_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> dict | None:
    """An endpoint for getting countries by id.

    Args:
        country_id (int): The country id.
        service (ICountryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if country does not exist.

    Returns:
        dict: The country attributes.
    """

    if country := await service.get_by_id(country_id):
        return country.model_dump()

    raise HTTPException(status_code=404, detail="Country not found")


@router.get(
        "/user/{user_id}",
        tags=['Country'],
        response_model=list[Country],
        status_code=200,
)
@inject
async def get_countries_by_user(
    user_id: UUID4,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries by user.

    Args:
        user_id (UUID4): The user id.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """

    countries = await service.get_by_user(user_id)

    return countries


@router.get(
        "/name/{name}",
        tags=['Country'],
        response_model=CountryDTO,
        status_code=200,
)
@inject
async def get_countries_by_name(
    name: str,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> dict | None:
    """An endpoint for getting country by name

    Args:
        name (str): The country name.
        service (ICountryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if country does not exist.

    Returns:
        dict: The country attributes.
    """
    if country := await service.get_by_name(name):
        return country.model_dump()

    raise HTTPException(status_code=404, detail="Country not found")


@router.get(
        "/inhabitants/{inhabitants}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def get_countries_by_inhabitants(
    inhabitants: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries by inhabitants.

    Args:
        inhabitants (int): The inhabitants of the country.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.get_by_inhabitants(inhabitants)

    return countries

@router.get(
        "/inhabitants/filter/{filter}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def filter_countries_by_inhabitants(
    inhabitants_start: int,
    inhabitants_stop: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries filter by inhabitants.

    Args:
        inhabitants_start (int): The minimum inhabitants of the country.
        inhabitants_stop (int): The maximum inhabitants of the country.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.filter_by_inhabitants(inhabitants_start, inhabitants_stop)

    return countries

@router.get(
        "/language/{language}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def get_countries_by_language(
    language: str,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries by language.

    Args:
        language (str): The language of the country.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.get_by_language(language)

    return countries

@router.get(
        "/area/{area}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def get_countries_by_area(
    area: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries by area.

    Args:
        area (int): The area of the country.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.get_by_area(area)

    return countries

@router.get(
        "/area/filter/{filter}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def filter_countries_by_area(
    area_start: int,
    area_stop: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries filter by area.

    Args:
        area_start (int): The minimum area of the country.
        area_stop (int): The maximum area of the country.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.filter_by_area(area_start, area_stop)

    return countries


@router.get(
        "/pkb/{pkb}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def get_countries_by_pkb(
    pkb: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries by pkb.

    Args:
        pkb (int): The pkb of the country.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.get_by_pkb(pkb)

    return countries

@router.get(
        "/pkb/filter/{filter}",
        tags=['Country'],
        response_model=Iterable[Country],
        status_code=200,
)
@inject
async def filter_countries_by_pkb(
    pkb_start: int,
    pkb_stop: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> Iterable:
    """An endpoint for getting countries filter by pkb.

    Args:
        pkb_start (int): The minimum pkb of the country.
        pkb_stop (int): The maximum pkb of the country.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        Iterable: The countries attributes collection.
    """
    countries = await service.filter_by_pkb(pkb_start, pkb_stop)

    return countries

