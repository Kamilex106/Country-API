"""Module containing country repository abstractions."""
from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

from countryapi.core.domain.country import CountryIn


class ICountryRepository(ABC):
    """An abstract class representing protocol of country repository."""
    @abstractmethod
    async def get_all_countries(self) -> Iterable[Any]:
        pass

    """The abstract getting all countries from the data storage.

    Returns:
        Iterable[Any]: The collection of the all countries.
    """

    @abstractmethod
    async def get_by_continent(self, continent_id: int) -> Iterable[Any]:
        pass

    """The abstract getting a country by continent from the data storage.

    Args:
        continent_id (int): The id of the continent.

    Returns:
        Iterable[Any]: The collection of the all countries by continent.
    """

    @abstractmethod
    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        pass

    """The abstract getting a country by user from the data storage.

    Args:
        user_id (UUID4): The user_id of the user.

    Returns:
        Iterable[Any]: The collection of the all countries by user_id.
    """

    @abstractmethod
    async def get_by_id(self, country_id: int) -> Any | None:
        pass

    """The abstract getting a country from the data storage.

    Args:
        country_id (int): The id of the country.

    Returns:
        Any | None: The country data if exists.
    """


    @abstractmethod
    async def get_by_name(self, name: str) -> Any | None:
        pass

    """The abstract getting a country by name from the data storage.

    Args:
        name (str): The name of the country.

    Returns:
        Any | None: The country data if exists.
    """


    @abstractmethod
    async def get_by_inhabitants(self, inhabitants: int) -> Iterable[Any]:
        pass

    """The abstract getting a country by inhabitants from the data storage.

    Args:
        inhabitants (int): Number of inhabitants of the country.

    Returns:
        Iterable[Any]: The collection of the all countries by inhabitants.
    """


    @abstractmethod
    async def get_by_language(self, language: str) -> Iterable[Any]:
        pass

    """The abstract getting a country by language from the data storage.

    Args:
        language (str): Official language of country.

    Returns:
        Iterable[Any]: The collection of the all countries by language.
    """

    @abstractmethod
    async def get_by_area(self, area: int) -> Iterable[Any]:
        pass

    """The abstract getting a country by area from the data storage.

    Args:
        area (int): Area of the country.

    Returns:
        Iterable[Any]: The collection of the all countries by area.
    """

    @abstractmethod
    async def get_by_pkb(self, pkb: int) -> Iterable[Any]:
        pass

    """The abstract getting a country by PKB from the data storage.

    Args:
        pkb (int): PKB of the country.

    Returns:
        Iterable[Any]: The collection of the all countries by pkb.
    """

    async def filter_by_pkb(self, pkb_start: int, pkb_stop: int) -> Iterable[Any]:
        pass

    """The abstract getting a country filter by pkb from the data storage.

    Args:
        pkb_start (int): Minimum PKB of the country.
        pkb_stop (int): Maximum PKB of the country.

    Returns:
        Iterable[Any]: The collection of the all countries by pkb.
    """


    async def filter_by_area(self, area_start: int, area_stop: int) -> Iterable[Any]:
        pass

    """The abstract getting a country filter by area from the data storage.

    Args:
        area_start (int): Minimum area of the country.
        area_stop (int): Maximum area of the country.

    Returns:
        Iterable[Any]: The collection of the all countries by area.
    """

    async def filter_by_inhabitants(self, inhabitants_start: int, inhabitants_stop: int) -> Iterable[Any]:
        pass

    """The abstract getting a country filter by inhabitants from the data storage.

    Args:
        inhabitants_start (int): Minimum number of inhabitants of the country.
        inhabitants_stop (int): Maximum number of inhabitants of the country.

    Returns:
        Iterable[Any]: The collection of the all countries by inhabitants.
    """


    @abstractmethod
    async def add_country(self, data: CountryIn) -> Any | None:
        pass

    """The abstract adding new country to the data storage.

    Args:
        data (CountryIn): The attributes of the country.

    Returns:
        Any | None: The newly created country.
    """


    @abstractmethod
    async def update_country(
        self,
        country_id: int,
        data: CountryIn,
    ) -> Any | None:
        pass

    """The abstract updating country data in the data storage.

    Args:
        country_id (int): The country id.
        data (CountryIn): The attributes of the country.

    Returns:
        Any | None: The updated country.
    """


    @abstractmethod
    async def delete_country(self, country_id: int) -> bool:
        pass
    """The abstract removing country from the data storage.

    Args:
        country_id (int): The country id.

    Returns:
        bool: Success of the operation.
    """
