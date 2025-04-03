"""Module containing favourite repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

from countryapi.core.domain.favourite import FavouriteIn


class IFavouriteRepository(ABC):
    """An abstract class representing protocol of favourite repository."""
    @abstractmethod
    async def get_favourite_by_id(self, favourite_id: int) -> Any | None:
        pass
    
    """The abstract getting a favourite from the data storage.

    Args:
        favourite_id (int): The id of the favourite.

    Returns:
        Any | None: The favourite data if exists.
    """


    @abstractmethod
    async def get_all_favourites(self) -> Iterable[Any]:
        pass
    
    """The abstract getting all favourites from the data storage.

    Returns:
        Iterable[Any]: The collection of the all favourites.
    """


    @abstractmethod
    async def get_favourite_by_country(self, country_name: str) -> Iterable[Any]:
        pass
    
    """The abstract getting a favourites by country from the data storage.

    Args:
        country_name (str): The country_name of the country.

    Returns:
        Iterable[Any]: The collection of the all favourites by country_name.
    """

    @abstractmethod
    async def get_favourite_by_user(self, user_id: UUID4) -> Iterable[Any]:
        pass
    
    """The abstract getting a favourite countries by user from the data storage.

    Args:
        user_id (UUID4): The user_id of the user.

    Returns:
        Iterable[Any]: The collection of the all favourites by user_id.
    """

    @abstractmethod
    async def add_favourite(self, data: FavouriteIn) -> Any | None:
        pass
    
    """The abstract adding new favourite to the data storage.

    Args:
        data (FavouriteIn): The attributes of the favourite.

    Returns:
        Any | None: The newly created favourite.
    """


    @abstractmethod
    async def update_favourite(
            self,
            favourite_id: int,
            data: FavouriteIn,
    ) -> Any | None:
        pass


    """The abstract updating favourite data in the data storage.

    Args:
        favourite_id (int): The favourite id.
        data (FavouriteIn): The attributes of the favourite.

    Returns:
        Any | None: The updated favourite.
    """

    @abstractmethod
    async def delete_favourite(self, favourite_id: int) -> bool:
        pass

    """The abstract removing favourite from the data storage.

    Args:
        favourite_id (int): The favourite id.

    Returns:
        bool: Success of the operation.
    """


