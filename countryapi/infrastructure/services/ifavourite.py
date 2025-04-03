"""Module containing favourite service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from countryapi.core.domain.favourite import Favourite, FavouriteIn


class IFavouriteService(ABC):
    """An abstract class representing protocol of favourite repository."""
    @abstractmethod
    async def get_favourite_by_id(self, favourite_id: int) -> Favourite | None:
        pass
    """The abstract getting a favourite from the repository.

    Args:
        favourite_id (int): The id of the favourite.

    Returns:
        Favourite | None: The favourite data if exists.
    """

    @abstractmethod
    async def get_all_favourites(self) -> Iterable[Favourite]:
        pass
    """The abstract getting all favourites from the repository.

    Returns:
        Iterable[Favourite]: The collection of the all favourites.
    """

    @abstractmethod
    async def get_ranking(self) -> list:
        pass
    """The abstract getting favourites ranking from the repository.

    Returns:
        list: The ranking of the all favourites.
    """

    @abstractmethod
    async def get_favourite_by_country(self, country_name: str) -> Iterable[Favourite]:
        pass
    """The abstract getting a favourite by country from the repository.

    Args:
        country_name (str): The country_name of the country.

    Returns:
        Iterable[Favourite]: The collection of the all favourites by country_name.
    """

    @abstractmethod
    async def get_favourite_by_user(self, user_id: UUID4) -> Iterable[Favourite]:
        pass
    """The abstract getting a favourite by user countries from the repository.

    Args:
        user_id (UUID4): The id of the user.

    Returns:
        Iterable[Favourite]: The collection of the all favourites by user_id.
    """


    @abstractmethod
    async def add_favourite(self, data: FavouriteIn) -> Favourite | None:
        pass
    """The abstract adding new favourite to the repository.

    Args:
        data (FavouriteIn): The attributes of the favourite.

    Returns:
        Favourite | None: The newly created favourite.
    """

    @abstractmethod
    async def update_favourite(
        self,
        favourite_id: int,
        data: FavouriteIn,
    ) -> Favourite | None:
        pass
    """The abstract updating favourite data in the repository.

    Args:
        favourite_id (int): The favourite id.
        data (FavouriteIn): The attributes of the favourite.

    Returns:
        Favourite | None: The updated favourite.
    """

    @abstractmethod
    async def delete_favourite(self, favourite_id: int) -> bool:
        pass
    """The abstract removing favourite from the repository.

    Args:
        favourite_id (int): The favourite id.

    Returns:
        bool: Success of the operation.
    """
