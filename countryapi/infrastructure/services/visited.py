"""Module containing visited service implementation."""
from typing import Iterable

from pydantic import UUID4

from countryapi.core.domain.visited import Visited, VisitedIn
from countryapi.core.repositories.ivisited import IVisitedRepository
from countryapi.infrastructure.services.ivisited import IVisitedService


class VisitedService(IVisitedService):
    """A class implementing the visited service."""
    _repository: IVisitedRepository

    def __init__(self, repository: IVisitedRepository) -> None:
        """The initializer of the `visited service`.

        Args:
            repository (IVisitedRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_visited_by_id(self, visited_id: int) -> Visited | None:
        """The abstract getting a visited from the repository.

        Args:
            visited_id (int): The id of the visited.

        Returns:
            Visited | None: The visited data if exists.
        """

        return await self._repository.get_visited_by_id(visited_id)
    
    async def get_all_visited(self) -> Iterable[Visited]:
        """The abstract getting all visited from the repository.

        Returns:
            Iterable[Visited]: The collection of the all visited.
        """
        return await self._repository.get_all_visited()

    async def get_visited_by_country(self, country_name: str) -> Iterable[Visited]:
        """The abstract getting a visited by country from the repository.

        Args:
            country_name (str): The name of the country.

        Returns:
            Iterable[Visited]: The collection of all visited by country_name.
        """
        return await self._repository.get_visited_by_country(country_name)


    async def get_visited_by_user(self, user_id: UUID4) -> Iterable[Visited]:
        """The abstract getting a visited countries by user from the repository.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            Iterable[Visited]: The collection of the all visited by user_id.
        """
        return await self._repository.get_visited_by_user(user_id)


    async def add_visited(self, data: VisitedIn) -> Visited | None:
        """The abstract adding new visited to the repository.

        Args:
            data (VisitedIn): The attributes of the visited.

        Returns:
            Visited | None: The newly created visited.
        """

        return await self._repository.add_visited(data)

    async def update_visited(
        self,
        visited_id: int,
        data: VisitedIn,
    ) -> Visited | None:
        """The abstract updating visited data in the repository.

        Args:
            visited_id (int): The visited id.
            data (VisitedIn): The attributes of the visited.

        Returns:
            Visited | None: The updated visited.
        """

        return await self._repository.update_visited(
            visited_id=visited_id,
            data=data,
        )

    async def delete_visited(self, visited_id: int) -> bool:
        """The abstract removing visited from the repository.

        Args:
            visited_id (int): The visited id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_visited(visited_id)
