"""Module containing visited repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

from countryapi.core.domain.visited import VisitedIn


class IVisitedRepository(ABC):
    """An abstract class representing protocol of visited repository."""
    @abstractmethod
    async def get_visited_by_id(self, visited_id: int) -> Any | None:
        pass
    
    """The abstract getting a visited from the data storage.

    Args:
        visited_id (int): The id of the visited.

    Returns:
        Any | None: The visited data if exists.
    """

    @abstractmethod
    async def get_all_visited(self) -> Iterable[Any]:
        pass

    """The abstract getting all visited from the data storage.

    Returns:
        Iterable[Any]: The collection of the all visited.
    """

    @abstractmethod
    async def get_visited_by_country(self, country_name: str) -> Iterable[Any]:
        pass
    
    """The abstract getting a visited countries by country name from the data storage.

    Args:
        country_name (str): The name of the country.

    Returns:
        Iterable[Any]: The collection of all visited by country_name.
    """

    @abstractmethod
    async def get_visited_by_user(self, user_id: UUID4) -> Iterable[Any]:
        pass

    """The abstract getting a visited countries by user from the data storage.

    Args:
        user_id (UUID4): The user_id of the user.

    Returns:
        Iterable[Any]: The collection of the all countries by user_id.
    """

    @abstractmethod
    async def add_visited(self, data: VisitedIn) -> Any | None:
        pass
    
    """The abstract adding new visited to the data storage.

    Args:
        data (VisitedIn): The attributes of the visited.

    Returns:
        Any | None: The newly created visited.
    """

    @abstractmethod
    async def update_visited(
            self,
            visited_id: int,
            data: VisitedIn,
    ) -> Any | None:
        pass
    
    """The abstract updating visited data in the data storage.

    Args:
        visited_id (int): The visited id.
        data (VisitedIn): The attributes of the visited.

    Returns:
        Any | None: The updated visited.
    """

    @abstractmethod
    async def delete_visited(self, visited_id: int) -> bool:
        pass
    
    """The abstract removing visited from the data storage.

    Args:
        visited_id (int): The visited id.

    Returns:
        bool: Success of the operation.
    """


 
