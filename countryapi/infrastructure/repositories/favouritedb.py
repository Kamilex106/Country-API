"""Module containing favourite database repository implementation."""
from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from pydantic import UUID4

from countryapi.core.domain.favourite import Favourite, FavouriteIn
from countryapi.core.repositories.ifavourite import IFavouriteRepository
from countryapi.db import favourite_table, database, user_table


class FavouriteRepository(IFavouriteRepository):
    """A class implementing the favourite repository."""

    async def get_favourite_by_id(self, favourite_id: int) -> Any | None:
        """The abstract getting a favourite from the data storage.

        Args:
            favourite_id (int): The id of the favourite.

        Returns:
            Any | None: The favourite data if exists.
        """

        favourite = await self._get_by_id(favourite_id)

        return Favourite(**dict(favourite)) if favourite else None

    async def get_all_favourites(self) -> Iterable[Any]:
        """The abstract getting all favourites from the data storage.

        Returns:
            Iterable[Any]: The collection of the all favourites.
        """

        query = favourite_table.select().order_by(favourite_table.c.id.asc())
        favourites = await database.fetch_all(query)

        return [Favourite(**dict(favourite)) for favourite in favourites]

    async def get_favourite_by_country(self, country_name: str) -> Iterable[Any]:
        """The abstract getting a favourite by country name from the data storage.

        Args:
            country_name (str): The name of the country.

        Returns:
            Iterable[Any]: The collection of the all favourites by country_name.
        """

        query = favourite_table \
            .select() \
            .where(favourite_table.c.country_name == country_name) \
            .order_by(favourite_table.c.country_name.asc())
        favourite = await database.fetch_all(query)

        return [Favourite(**dict(fav)) for fav in favourite]


    async def get_favourite_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The abstract getting a favourite countries by user from the data storage.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            Iterable[Any]: The collection of the all favourites by user_id.
        """

        query = favourite_table \
            .select() \
            .where(favourite_table.c.user_id == user_id) \
            .order_by(favourite_table.c.user_id.asc())
        favourite = await database.fetch_all(query)

        return [Favourite(**dict(fav)) for fav in favourite]


    async def add_favourite(self, data: FavouriteIn) -> Any | None:
        """The abstract adding new favourite to the data storage.

        Args:
            data (FavouriteIn): The attributes of the favourite.

        Returns:
            Any | None: The newly created favourite.
        """

        query = favourite_table.insert().values(**data.model_dump())
        new_favourite_id = await database.execute(query)
        new_favourite = await self._get_by_id(new_favourite_id)

        return Favourite(**dict(new_favourite)) if new_favourite else None

    async def update_favourite(
        self,
        favourite_id: int,
        data: FavouriteIn,
    ) -> Any | None:
        """The abstract updating favourite data in the data storage.

        Args:
            favourite_id (int): The favourite id.
            data (FavouriteIn): The attributes of the favourite.

        Returns:
            Any | None: The updated favourite.
        """

        if self._get_by_id(favourite_id):
            query = (
                favourite_table.update()
                .where(favourite_table.c.id == favourite_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            favourite = await self._get_by_id(favourite_id)

            return Favourite(**dict(favourite)) if favourite else None

        return None

    async def delete_favourite(self, favourite_id: int) -> bool:
        """The abstract removing favourite from the data storage.

        Args:
            favourite_id (int): The favourite id.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(favourite_id):
            query = favourite_table \
                .delete() \
                .where(favourite_table.c.id == favourite_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, favourite_id: int) -> Record | None:
        """A private method getting favourite from the DB based on its ID.

        Args:
            favourite_id (int): The ID of the favourite.

        Returns:
            Record | None: Favourite record if exists.
        """


        query = (
            favourite_table.select()
            .where(favourite_table.c.id == favourite_id)
        )

        return await database.fetch_one(query)
