"""Module containing visited database repository implementation."""
from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from pydantic import UUID4

from countryapi.core.domain.visited import Visited, VisitedIn
from countryapi.core.repositories.ivisited import IVisitedRepository
from countryapi.db import visited_table, database

class VisitedRepository(IVisitedRepository):
    """A class implementing the visited repository."""

    async def get_visited_by_id(self, visited_id: int) -> Any | None:
        """The abstract getting a visited from the data storage.

        Args:
            visited_id (int): The id of the visited.

        Returns:
            Any | None: The visited data if exists.
        """

        visited = await self._get_by_id(visited_id)

        return Visited(**dict(visited)) if visited else None

    async def get_all_visited(self) -> Iterable[Any]:
        """The abstract getting all visited from the data storage.

        Returns:
            Iterable[Any]: The collection of the all visited.
        """

        query = visited_table.select().order_by(visited_table.c.id.asc())
        visited = await database.fetch_all(query)

        return [Visited(**dict(visit)) for visit in visited]

    async def get_visited_by_country(self, country_name: str) -> Iterable[Any]:
        """The abstract getting a visited by country from the data storage.

        Args:
            country_name (str): The name of the country.

        Returns:
            Iterable[Any]: The collection of all visited by country_name.
        """

        query = visited_table \
            .select() \
            .where(visited_table.c.country_name == country_name) \
            .order_by(visited_table.c.country_name.asc())
        visited = await database.fetch_all(query)

        return [Visited(**dict(visit)) for visit in visited]


    async def get_visited_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The abstract getting a visited countries by user from the data storage.

        Args:
            user_id (UUID4): The user_id of the user.

        Returns:
            Iterable[Any]: The collection of the all countries by user_id.
        """

        query = visited_table \
            .select() \
            .where(visited_table.c.user_id == user_id) \
            .order_by(visited_table.c.user_id.asc())
        visited = await database.fetch_all(query)

        return [Visited(**dict(visit)) for visit in visited]


    async def add_visited(self, data: VisitedIn) -> Any | None:
        """The abstract adding new visited to the data storage.

        Args:
            data (VisitedIn): The attributes of the visited.

        Returns:
            Any | None: The newly created visited.
        """

        query = visited_table.insert().values(**data.model_dump())
        new_visited_id = await database.execute(query)
        new_visited = await self._get_by_id(new_visited_id)

        return Visited(**dict(new_visited)) if new_visited else None

    async def update_visited(
        self,
        visited_id: int,
        data: VisitedIn,
    ) -> Any | None:
        """The abstract updating visited data in the data storage.

        Args:
            visited_id (int): The visited id.
            data (VisitedIn): The attributes of the visited.

        Returns:
            Any | None: The updated visited.
        """

        if self._get_by_id(visited_id):
            query = (
                visited_table.update()
                .where(visited_table.c.id == visited_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            visited = await self._get_by_id(visited_id)

            return Visited(**dict(visited)) if visited else None

        return None

    async def delete_visited(self, visited_id: int) -> bool:
        """The abstract removing visited from the data storage.

        Args:
            visited_id (int): The visited id.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(visited_id):
            query = visited_table \
                .delete() \
                .where(visited_table.c.id == visited_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, visited_id: int) -> Record | None:
        """A private method getting visited from the DB based on its ID.

        Args:
            visited_id (int): The ID of the visited.

        Returns:
            Record | None: Visited record if exists.
        """


        query = (
            visited_table.select()
            .where(visited_table.c.id == visited_id)
        )

        return await database.fetch_one(query)
