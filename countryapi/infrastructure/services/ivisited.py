"""Module containing visited service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from countryapi.core.domain.visited import Visited, VisitedIn


class IVisitedService(ABC):
    """An abstract class representing protocol of visited repository."""
    @abstractmethod
    async def get_visited_by_id(self, visited_id: int) -> Visited | None:
        pass
    """The abstract getting a visited from the repository.

    Args:
        visited_id (int): The id of the visited.

    Returns:
        Visited | None: The visited data if exists.
    """

    @abstractmethod
    async def get_all_visited(self) -> Iterable[Visited]:
        pass
    """The abstract getting all visited from the repository.

    Returns:
        Iterable[Visited]: The collection of the all visited.
    """
    
    
    @abstractmethod
    async def get_visited_by_country(self, country_name: str) -> Iterable[Visited]:
        pass
    """The abstract getting a visited by country from the repository.

    Args:
        country_name (str): The name of the country.

    Returns:
        Iterable[Visited]: The collection of all visited by country_name.
    """

    @abstractmethod
    async def get_visited_by_user(self, user_id: UUID4) -> Iterable[Visited]:
        pass
    """The abstract getting a visited countries by user from the repository.

    Args:
        user_id (UUID4): The id of the user.

    Returns:
        Iterable[Visited]: The collection of the all visited by user_id.
    """

    @abstractmethod
    async def add_visited(self, data: VisitedIn) -> Visited | None:
        pass
    """The abstract adding new visited to the repository.

    Args:
        data (VisitedIn): The attributes of the visited.

    Returns:
        Visited | None: The newly created visited.
    """

    @abstractmethod
    async def update_visited(
        self,
        visited_id: int,
        data: VisitedIn,
    ) -> Visited | None:
        pass
    """The abstract updating visited data in the repository.

    Args:
        visited_id (int): The visited id.
        data (VisitedIn): The attributes of the visited.

    Returns:
        Visited | None: The updated visited.
    """

    @abstractmethod
    async def delete_visited(self, visited_id: int) -> bool:
        pass
    """The abstract removing visited from the repository.

    Args:
        visited_id (int): The visited id.

    Returns:
        bool: Success of the operation.
    """

