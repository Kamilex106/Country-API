"""Module containing favourite service implementation."""
from typing import Iterable

from pydantic import UUID4

from countryapi.core.domain.favourite import Favourite, FavouriteIn
from countryapi.core.repositories.ifavourite import IFavouriteRepository
from countryapi.infrastructure.services.ifavourite import IFavouriteService


class FavouriteService(IFavouriteService):
    """A class implementing the favourite service."""
    _repository: IFavouriteRepository

    def __init__(self, repository: IFavouriteRepository) -> None:
        """The initializer of the `favourite service`.

        Args:
            repository (IFavouriteRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_favourite_by_id(self, favourite_id: int) -> Favourite | None:
        """The abstract getting a favourite from the repository.

        Args:
            favourite_id (int): The id of the favourite.

        Returns:
            Favourite | None: The favourite data if exists.
        """
        return await self._repository.get_favourite_by_id(favourite_id)

    async def get_all_favourites(self) -> Iterable[Favourite]:
        """The abstract getting all favourites from the repository.

        Returns:
            Iterable[Favourite]: The collection of the all favourites.
        """
        return await self._repository.get_all_favourites()

    async def get_ranking(self) -> list:
        """The abstract getting favourites ranking from the repository.

        Returns:
            list: The ranking of the all favourites.
        """
        all_favourites =  await self._repository.get_all_favourites()
        countries = {}

        for favourite in all_favourites:
            country_name = favourite.country_name

            if countries.get(country_name) is None:
                countries[country_name] = 1
            else:
                countries[country_name] += 1

        sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
        return sorted_countries



    async def get_favourite_by_country(self, country_name: str) -> Iterable[Favourite]:
        """The abstract getting a favourite by country from the repository.

        Args:
            country_name (str): The name of the country.

        Returns:
            Iterable[Favourite]: The collection of the all favourites by country_name.
        """
        return await self._repository.get_favourite_by_country(country_name)


    async def get_favourite_by_user(self, user_id: UUID4) -> Iterable[Favourite]:
        """The abstract getting a favourite countries by user from the repository.

        Args:
            user_id (UUID4): The id of the user.

        Returns:
            Iterable[Favourite]: The collection of the all favourites by user_id.
        """
        return await self._repository.get_favourite_by_user(user_id)


    async def add_favourite(self, data: FavouriteIn) -> Favourite | None:
        """The abstract adding new favourite to the repository.

        Args:
            data (FavouriteIn): The attributes of the favourite.

        Returns:
            Favourite | None: The newly created favourite.
        """
        return await self._repository.add_favourite(data)

    async def update_favourite(
        self,
        favourite_id: int,
        data: FavouriteIn,
    ) -> Favourite | None:
        """The abstract updating favourite data in the repository.

        Args:
            favourite_id (int): The favourite id.
            data (FavouriteIn): The attributes of the favourite.

        Returns:
            Favourite | None: The updated favourite.
        """

        return await self._repository.update_favourite(
            favourite_id=favourite_id,
            data=data,
        )

    async def delete_favourite(self, favourite_id: int) -> bool:
        """The abstract removing favourite from the repository.

        Args:
            favourite_id (int): The favourite id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_favourite(favourite_id)
