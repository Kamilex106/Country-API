"""Module containing country database repository implementation."""
from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from pydantic import UUID4
from sqlalchemy import select, join

from countryapi.core.repositories.icountry import ICountryRepository
from countryapi.core.domain.country import Country, CountryIn
from countryapi.db import (
    country_table,
    continent_table,
    user_table,
    database,
)
from countryapi.infrastructure.dto.countrydto import CountryDTO


class CountryRepository(ICountryRepository):
    """A class implementing the country repository."""
    async def get_all_countries(self) -> Iterable[Any]:
        """The abstract getting all countries from the data storage.

        Returns:
            Iterable[Any]: The collection of the all continents.
        """

        query = (
            select(country_table, continent_table, user_table)
            .select_from(
                join(
                    join(
                        country_table,
                        continent_table,
                        country_table.c.continent_id == continent_table.c.id
                    ),
                    user_table,
                    country_table.c.user_id == user_table.c.id
                )
            )
            .order_by(country_table.c.name.asc())
        )
        countries = await database.fetch_all(query)

        return [CountryDTO.from_record(country) for country in countries]


    async def get_by_continent(self, continent_id: int) -> Iterable[Any]:
        """The abstract getting a country by continent from the data storage.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Any]: The collection of the all countries by continent.
        """

        query = country_table \
            .select() \
            .where(country_table.c.continent_id == continent_id) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]


    async def get_by_id(self, country_id: int) -> Any | None:
        """The abstract getting a country from the data storage.

        Args:
            country_id (int): The id of the country.

        Returns:
            Any | None: The country data if exists.
        """

        query = (
            select(country_table, continent_table, user_table)
            .select_from(
                join(
                    join(
                        country_table,
                        continent_table,
                        country_table.c.continent_id == continent_table.c.id
                    ),
                    user_table,
                    country_table.c.user_id == user_table.c.id
                )
            )
            .where(country_table.c.id == country_id)
            .order_by(country_table.c.name.asc())
        )
        country = await database.fetch_one(query)

        return CountryDTO.from_record(country) if country else None


    async def get_by_name(self, name: str) -> Any | None:
        """The abstract getting a country by name from the data storage.

        Args:
            name (str): The name of the country.

        Returns:
            Any | None: The country data if exists.
        """

        query = (
            select(country_table, continent_table, user_table)
            .select_from(
                join(
                    join(
                        country_table,
                        continent_table,
                        country_table.c.continent_id == continent_table.c.id
                    ),
                    user_table,
                    country_table.c.user_id == user_table.c.id
                )
            )
            .where(country_table.c.name == name)
            .order_by(country_table.c.name.asc())
        )
        country = await database.fetch_one(query)

        return CountryDTO.from_record(country) if country else None


    async def get_by_inhabitants(self, inhabitants: int) -> Iterable[Any]:
        """The abstract getting a country by inhabitants from the data storage.

        Args:
            inhabitants (int): Number of inhabitants of the country.

        Returns:
            Iterable[Any]: The collection of the all countries by inhabitants.
        """

        query = country_table \
            .select() \
            .where(country_table.c.inhabitants == inhabitants) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]


    async def get_by_language(self, language: str) -> Iterable[Any]:
        """The abstract getting a country by language from the data storage.

        Args:
            language (str): Official language of country.

        Returns:
            Iterable[Any]: The collection of the all countries by language.
        """

        query = country_table \
            .select() \
            .where(country_table.c.language == language) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]


    async def get_by_area(self, area: int) -> Iterable[Any]:
        """The abstract getting a country by area from the data storage.

        Args:
            area (int): Area of the country.

        Returns:
            Iterable[Any]: The collection of the all countries by area.
        """

        query = country_table \
            .select() \
            .where(country_table.c.area == area) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]


    async def get_by_pkb(self, pkb: int) -> Iterable[Any]:
        """The abstract getting a country by PKB from the data storage.

        Args:
            pkb (int): PKB of the country.

        Returns:
            Iterable[Any]: The collection of the all countries by pkb.
        """

        query = country_table \
            .select() \
            .where(country_table.c.pkb == pkb) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]

    async def filter_by_pkb(self, pkb_start: int, pkb_stop: int) -> Iterable[Any]:
        """The abstract getting a country filter by PKB from the data storage.

        Args:
            pkb_start (int): Minimum PKB of the country.
            pkb_stop (int): Maximum PKB of the country.

        Returns:
            Iterable[Any]: The collection of the all countries by pkb.
        """

        query = country_table \
            .select() \
            .where(country_table.c.pkb >= pkb_start) \
            .where(country_table.c.pkb <= pkb_stop) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]

    async def filter_by_area(self, area_start: int, area_stop: int) -> Iterable[Any]:
        """The abstract getting a country filter by area from the data storage.

        Args:
            area_start (int): Minimum area of the country.
            area_stop (int): Maximum area of the country.

        Returns:
            Iterable[Any]: The collection of the all countries by area.
        """

        query = country_table \
            .select() \
            .where(country_table.c.area >= area_start) \
            .where(country_table.c.area <= area_stop) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]

    async def filter_by_inhabitants(self, inhabitants_start: int, inhabitants_stop: int) -> Iterable[Any]:
        """The abstract getting a country filter by inhabitants from the data storage.

        Args:
            inhabitants_start (int): Minimum number of inhabitants of the country.
            inhabitants_stop (int): Maximum number of inhabitants of the country.

        Returns:
            Iterable[Any]: The collection of the all countries by inhabitants.
        """

        query = country_table \
            .select() \
            .where(country_table.c.inhabitants >= inhabitants_start) \
            .where(country_table.c.inhabitants <= inhabitants_stop) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]

    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The abstract getting a country by user from the data storage.

        Args:
            user_id (UUID4): The user_id of the user.

        Returns:
            Iterable[Any]: The collection of the all countries by user_id.
        """

        query = country_table \
            .select() \
            .where(country_table.c.user_id == user_id) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]

    async def add_country(self, data: CountryIn) -> Any | None:
        """The abstract adding new country to the data storage.

        Args:
            data (CountryIn): The attributes of the country.

        Returns:
            Any | None: The newly created country.
        """

        if await self._get_continent_by_id(data.continent_id):
            if await self.get_by_name(data.name):
                return None
            query = country_table.insert().values(**data.model_dump())
            new_country_id = await database.execute(query)
            new_country = await self._get_by_id(new_country_id)
            return Country(**dict(new_country))

        return None

    async def update_country(
        self,
        country_id: int,
        data: CountryIn,
    ) -> Any | None:
        """The abstract updating country data in the data storage.

        Args:
            country_id (int): The country id.
            data (CountryIn): The attributes of the country.

        Returns:
            Any | None: The updated country.
        """

        if self._get_by_id(country_id):
            if await self._get_continent_by_id(data.continent_id):
                query = (
                    country_table.update()
                    .where(country_table.c.id == country_id)
                    .values(**data.model_dump())
                )
                await database.execute(query)

                country = await self._get_by_id(country_id)

                return Country(**dict(country)) if country else None

        return None

    async def delete_country(self, country_id: int) -> bool:
        """The abstract removing country from the data storage.

        Args:
            country_id (int): The country id.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(country_id):
            query = country_table \
                .delete() \
                .where(country_table.c.id == country_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, country_id: int) -> Record | None:
        """A private method getting country from the DB based on its ID.

        Args:
            country_id (int): The ID of the country.

        Returns:
            Record | None: Country record if exists.
        """

        query = (
            country_table.select()
            .where(country_table.c.id == country_id)
            .order_by(country_table.c.name.asc())
        )

        return await database.fetch_one(query)

    async def _get_continent_by_id(self, continent_id: int) -> Record | None:
        """A private method getting continent from the DB based on its ID.

        Args:
            continent_id (int): The ID of the continent.

        Returns:
            Record | None: Continent record if exists.
        """

        query = (
            continent_table.select()
            .where(continent_table.c.id == continent_id)
            .order_by(continent_table.c.name.asc())
        )

        return await database.fetch_one(query)
