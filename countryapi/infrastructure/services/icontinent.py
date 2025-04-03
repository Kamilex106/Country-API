"""Module containing continent service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable

from countryapi.core.domain.location import Continent, ContinentIn


class IContinentService(ABC):
    """An abstract class representing protocol of continent repository."""
    @abstractmethod
    async def get_continent_by_id(self, continent_id: int) -> Continent | None:
        pass
    """The abstract getting a continent from the repository.

    Args:
        continent_id (int): The id of the continent.

    Returns:
        Continent | None: The continent data if exists.
    """

    @abstractmethod
    async def get_continent_by_alias(self, alias: str) -> Continent | None:
        pass
    """The abstract getting a continent by alias from the repository.

    Args:
        alias (str): The alias of the continent.

    Returns:
        Continent | None: The continent data if exists.
    """

    @abstractmethod
    async def get_all_continents(self) -> Iterable[Continent]:
        pass
    """The abstract getting all continents from the repository.

    Returns:
        Iterable[Continent]: The collection of the all continents.
    """


    @abstractmethod
    async def add_continent(self, data: ContinentIn) -> Continent | None:
        pass
    """The abstract adding new continent to the repository.

    Args:
        data (ContinentIn): The attributes of the continent.

    Returns:
        Continent | None: The newly created continent.
    """


    @abstractmethod
    async def update_continent(
        self,
        continent_id: int,
        data: ContinentIn,
    ) -> Continent | None:
        pass
    """The abstract updating continent data in the repository.

    Args:
        continent_id (int): The continent id.
        data (ContinentIn): The attributes of the continent.

    Returns:
        Continent | None: The updated continent.
    """

    @abstractmethod
    async def delete_continent(self, continent_id: int) -> bool:
        pass
    """The abstract removing continent from the repository.

    Args:
        continent_id (int): The continent id.

    Returns:
        bool: Success of the operation.
    """