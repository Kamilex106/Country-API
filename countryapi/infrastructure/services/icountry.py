"""Module containing country service abstractions."""
from abc import ABC, abstractmethod
from typing import Iterable, Any

from pydantic import UUID4

from countryapi.core.domain.country import Country, CountryIn
from countryapi.infrastructure.dto.countrydto import CountryDTO


class ICountryService(ABC):
    """An abstract class representing protocol of country repository."""
    @abstractmethod
    async def get_all(self) -> Iterable[CountryDTO]:
        pass
    """The abstract getting all countries from the repository.

    Returns:
        Iterable[CountryDTO]: The collection of the all countries.
    """

    @abstractmethod
    async def get_summary_by_continent(self, continent_id: int) -> dict:
        pass
    """The abstract getting a summary by continent from the repository.

    Args:
        continent_id (int): The id of the continent.

    Returns:
        dict: The summary of the all countries by continent.
    """

    @abstractmethod
    async def get_summary_by_all_continents(self) -> dict:
        pass
    """The abstract getting a summary by all continents from the repository.

    Returns:
        dict: The summary of the all countries by continent.
    """

    @abstractmethod
    async def get_by_continent(self, continent_id: int) -> Iterable[Country]:
        pass
    """The abstract getting a country by continent from the repository.

    Args:
        continent_id (int): The id of the continent.

    Returns:
        Iterable[Country]: The collection of the all countries by continent.
    """

    @abstractmethod
    async def get_by_id(self, country_id: int) -> CountryDTO | None:
        pass
    """The abstract getting a country from the repository.

    Args:
        country_id (int): The id of the country.

    Returns:
        CountryDTO | None: The country data if exists.
    """

    @abstractmethod
    async def get_by_name(self, name: str) -> CountryDTO | None:
        pass
    """The abstract getting a country by name from the repository.

    Args:
        name (str): The name of the country.

    Returns:
        CountryDTO | None: The country data if exists.
    """


    @abstractmethod
    async def get_by_inhabitants(self, inhabitants: int) -> Iterable[Country]:
        pass
    """The abstract getting a country by inhabitants from the repository.

    Args:
        inhabitants (int): Number of inhabitants of the country.

    Returns:
        Iterable[Country]: The collection of the all countries by inhabitants.
    """

    @abstractmethod
    async def get_by_language(self, language: str) -> Iterable[Country]:
        pass
    """The abstract getting a country by language from the repository.

    Args:
        language (str): Official language of country.

    Returns:
        Iterable[Country]: The collection of the all countries by language.
    """

    @abstractmethod
    async def get_by_area(self, area: int) -> Iterable[Country]:
        pass
    """The abstract getting a country by area from the repository.

    Args:
        area (int): Area of the country.

    Returns:
        Iterable[Country]: The collection of the all countries by area.
    """

    @abstractmethod
    async def get_by_pkb(self, pkb: int) -> Iterable[Country]:
        pass
    """The abstract getting a country by PKB from the repository.

    Args:
        pkb (int): PKB of the country.

    Returns:
        Iterable[Country]: The collection of the all countries by pkb.
    """

    @abstractmethod
    async def filter_by_pkb(self, pkb_start: int, pkb_stop: int) -> Iterable[Country]:
        pass
    """The abstract getting a country filter by PKB from the repository.

    Args:
        pkb_start (int): Minimum PKB of the country.
        pkb_stop (int): Maximum PKB of the country.

    Returns:
        Iterable[Country]: The collection of the all countries by pkb.
    """

    @abstractmethod
    async def filter_by_area(self, area_start: int, area_stop: int) -> Iterable[Country]:
        pass
    """The abstract getting a country filter by area from the repository.

    Args:
        area_start (int): Minimum area of the country.
        area_stop (int): Maximum area of the country.

    Returns:
        Iterable[Country]: The collection of the all countries by area.
    """

    @abstractmethod
    async def filter_by_inhabitants(self, inhabitants_start: int, inhabitants_stop: int) -> Iterable[Country]:
        pass
    """The abstract getting a country filter by inhabitants from the repository.

    Args:
        inhabitants_start (int): Minimum number of inhabitants of the country.
        inhabitants_stop (int): Maximum number of inhabitants of the country.

    Returns:
        Iterable[Country]: The collection of the all countries by inhabitants.
    """

    @abstractmethod
    async def get_by_user(self, user_id: UUID4) -> Iterable[Country]:
        pass
    """The abstract getting a country by user from the repository.

    Args:
        user_id (UUID4): The id of the user.

    Returns:
        Iterable[Country]: The collection of the all countries by user_id.
    """

    @abstractmethod
    async def add_country(self, data: CountryIn) -> Country | None:
        pass
    """The abstract adding new country to the repository.

    Args:
        data (CountryIn): The attributes of the country.

    Returns:
        Country | None: The newly created country.
    """


    @abstractmethod
    async def update_country(
        self,
        country_id: int,
        data: CountryIn,
    ) -> Country | None:
        pass
    """The abstract updating country data in the repository.

    Args:
        country_id (int): The country id.
        data (CountryIn): The attributes of the country.

    Returns:
        Country | None: The updated country.
    """

    @abstractmethod
    async def delete_country(self, country_id: int) -> bool:
        pass
    """The abstract removing country from the repository.

    Args:
        country_id (int): The country id.

    Returns:
        bool: Success of the operation.
    """