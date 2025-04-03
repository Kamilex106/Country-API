"""Module containing country service implementation."""
from typing import Iterable

from pydantic import UUID4

from countryapi.core.domain.country import Country, CountryIn
from countryapi.core.repositories.icountry import ICountryRepository
from countryapi.infrastructure.dto.countrydto import CountryDTO
from countryapi.infrastructure.services.icountry import ICountryService


class CountryService(ICountryService):
    """A class implementing the country service."""
    _repository: ICountryRepository

    def __init__(self, repository: ICountryRepository) -> None:
        """The initializer of the `country service`.

        Args:
            repository (ICountryRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_all(self) -> Iterable[CountryDTO]:
        """The abstract getting all countries from the repository.

        Returns:
            Iterable[CountryDTO]: The collection of the all countries.
        """
        return await self._repository.get_all_countries()

    async def get_summary_by_continent(self, continent_id: int) -> dict:
        """The abstract getting a summary by continent from the repository.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            dict: The summary of the all countries by continent.
        """

        continent = await self._repository.get_by_continent(continent_id)
        countries = {}
        inhabitants = 0
        area = 0
        pkb = 0
        i = 0
        for country in continent:
            inhabitants += country.inhabitants
            area += country.area
            pkb += country.pkb
            i += 1

        if i==0:
            i=1
        av_inhabitants = inhabitants / i
        av_area = area / i
        av_pkb = pkb / i
        countries['average inhabitants'] = av_inhabitants
        countries['average area'] = av_area
        countries['average pkb'] = av_pkb
        countries['all inhabitants'] = inhabitants
        countries['all area'] = area
        countries['all pkb'] = pkb

        return countries

    async def get_summary_by_all_continents(self) -> dict:
        """The abstract getting a summary by all continents from the repository.

        Returns:
            dict: The summary of the all countries by continent.
        """
        all_id = set()
        countries = {}
        all_countries = await self.get_all()
        for country in all_countries:
            all_id.add(country.continent.id)

        for id in all_id:
            continent = await self._repository.get_by_continent(id)
            inhabitants = 0
            area = 0
            pkb = 0
            i = 0
            for country in continent:
                inhabitants += country.inhabitants
                area += country.area
                pkb += country.pkb
                i += 1

            if i == 0:
                i = 1
            av_inhabitants = inhabitants / i
            av_area = area / i
            av_pkb = pkb / i
            countries[id]={}
            countries[id]['average inhabitants'] = av_inhabitants
            countries[id]['average area'] = av_area
            countries[id]['average pkb'] = av_pkb
            countries[id]['all inhabitants'] = inhabitants
            countries[id]['all area'] = area
            countries[id]['all pkb'] = pkb


        return countries


    async def get_by_continent(self, continent_id: int) -> Iterable[Country]:
        """The abstract getting a country by continent from the repository.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Country]: The collection of the all countries by continent.
        """
        return await self._repository.get_by_continent(continent_id)

    async def get_by_id(self, country_id: int) -> CountryDTO | None:
        """The abstract getting a country from the repository.

        Args:
            country_id (int): The id of the country.

        Returns:
            CountryDTO | None: The country data if exists.
        """
        return await self._repository.get_by_id(country_id)


    async def get_by_user(self, user_id: UUID4) -> Iterable[Country]:
        """The abstract getting a country by user from the repository.

        Args:
            user_id (UUID4): The user_id of the user.

        Returns:
            Iterable[Country]: The collection of the all countries by user_id.
        """
        return await self._repository.get_by_user(user_id)


    async def get_by_name(self, name: str) -> CountryDTO | None:
        """The abstract getting a country by name from the repository.

        Args:
            name (str): The name of the country.

        Returns:
            CountryDTO | None: The country data if exists.
        """
        return await self._repository.get_by_name(name)


    async def get_by_inhabitants(self, inhabitants: int) -> Iterable[Country]:
        """The abstract getting a country by inhabitants from the repository.

        Args:
            inhabitants (int): Number of inhabitants of the country.

        Returns:
            Iterable[Country]: The collection of the all countries by inhabitants.
        """
        return await self._repository.get_by_inhabitants(inhabitants)


    async def get_by_language(self, language: str) -> Iterable[Country]:
        """The abstract getting a country by language from the repository.

        Args:
            language (str): Official language of country.

        Returns:
            Iterable[Country]: The collection of the all countries by language.
        """
        return await self._repository.get_by_language(language)


    async def get_by_area(self, area: int) -> Iterable[Country]:
        """The abstract getting a country by area from the repository.

        Args:
            area (int): Area of the country.

        Returns:
            Iterable[Country]: The collection of the all countries by area.
        """
        return await self._repository.get_by_area(area)

    async def get_by_pkb(self, pkb: int) -> Iterable[Country]:
        """The abstract getting a country by PKB from the repository.

        Args:
            pkb (int): PKB of the country.

        Returns:
            Iterable[Country]: The collection of the all countries by pkb.
        """

        return await self._repository.get_by_pkb(pkb)

    async def filter_by_pkb(self, pkb_start: int, pkb_stop: int) -> Iterable[Country]:
        """The abstract getting a country filter by PKB from the repository.

        Args:
            pkb_start (int): Minimum PKB of the country.
            pkb_stop (int): Maximum PKB of the country.

        Returns:
            Iterable[Country]: The collection of the all countries by pkb.
        """
        return await self._repository.filter_by_pkb(pkb_start,pkb_stop)


    async def filter_by_area(self, area_start: int, area_stop: int) -> Iterable[Country]:
        """The abstract getting a country filter by area from the repository.

        Args:
            area_start (int): Minimum area of the country.
            area_stop (int): Maximum area of the country.

        Returns:
            Iterable[Country]: The collection of the all countries by area.
        """
        return await self._repository.filter_by_area(area_start,area_stop)


    async def filter_by_inhabitants(self, inhabitants_start: int, inhabitants_stop: int) -> Iterable[Country]:
        """The abstract getting a country filter by inhabitants from the repository.

        Args:
            inhabitants_start (int): Minimum number of inhabitants of the country.
            inhabitants_stop (int): Maximum number of inhabitants of the country.

        Returns:
            Iterable[Country]: The collection of the all countries by inhabitants.
        """
        return await self._repository.filter_by_inhabitants(inhabitants_start,inhabitants_stop)
    

    async def add_country(self, data: CountryIn) -> Country | None:
        """The abstract adding new country to the repository.

        Args:
            data (CountryIn): The attributes of the country.

        Returns:
            Country | None: The newly created country.
        """

        return await self._repository.add_country(data)


    async def update_country(
        self,
        country_id: int,
        data: CountryIn,
    ) -> Country | None:
        """The abstract updating country data in the repository.

        Args:
            country_id (int): The country id.
            data (CountryIn): The attributes of the country.

        Returns:
            Country | None: The updated country.
        """

        return await self._repository.update_country(
            country_id=country_id,
            data=data,
        )

    async def delete_country(self, country_id: int) -> bool:
        """The abstract removing country from the repository.

        Args:
            country_id (int): The country id.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_country(country_id)
