"""Module containing continent service implementation."""
from typing import Iterable

from countryapi.core.domain.location import Continent, ContinentIn
from countryapi.core.repositories.icontinent import IContinentRepository
from countryapi.infrastructure.services.icontinent import IContinentService


class ContinentService(IContinentService):
    """A class implementing the continent service."""

    _repository: IContinentRepository

    def __init__(self, repository: IContinentRepository) -> None:
        """The initializer of the `continent service`.

        Args:
            repository (IContinentRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_continent_by_id(self, continent_id: int) -> Continent | None:
        """The abstract getting a continent from the repository.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Continent | None: The continent data if exists.
        """
        return await self._repository.get_continent_by_id(continent_id)

    async def get_continent_by_alias(self, alias: str) -> Continent | None:
        """The abstract getting a continent by alias from the repository.

        Args:
            alias (str): The alias of the continent.

        Returns:
            Continent | None: The continent data if exists.
        """
        return await self._repository.get_continent_by_alias(alias)

    async def get_all_continents(self) -> Iterable[Continent]:
        """The abstract getting all continents from the repository.

        Returns:
            Iterable[Continent]: The collection of the all continents.
        """
        return await self._repository.get_all_continents()

    async def add_continent(self, data: ContinentIn) -> Continent | None:
        """The abstract adding new continent to the repository.

        Args:
            data (ContinentIn): The attributes of the continent.

        Returns:
            Continent | None: The newly created continent.
        """
        return await self._repository.add_continent(data)

    async def update_continent(
        self,
        continent_id: int,
        data: ContinentIn,
    ) -> Continent | None:
        """The abstract updating continent data in the repository.

        Args:
            continent_id (int): The continent id.
            data (ContinentIn): The attributes of the continent.

        Returns:
            Continent | None: The updated continent.
        """

        return await self._repository.update_continent(
            continent_id=continent_id,
            data=data,
        )

    async def delete_continent(self, continent_id: int) -> bool:
        """The abstract removing continent from the repository.

        Args:
            continent_id (int): The continent id.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_continent(continent_id)
