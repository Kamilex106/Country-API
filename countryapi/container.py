"""Module providing containers injecting dependencies."""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from countryapi.infrastructure.repositories.countrydb import CountryRepository
from countryapi.infrastructure.repositories.continentdb import ContinentRepository
from countryapi.infrastructure.repositories.user import UserRepository
from countryapi.infrastructure.repositories.visiteddb import VisitedRepository
from countryapi.infrastructure.repositories.favouritedb import FavouriteRepository


from countryapi.infrastructure.services.country import CountryService
from countryapi.infrastructure.services.continent import ContinentService
from countryapi.infrastructure.services.user import UserService
from countryapi.infrastructure.services.visited import VisitedService
from countryapi.infrastructure.services.favourite import FavouriteService



class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    continent_repository = Singleton(ContinentRepository)
    user_repository = Singleton(UserRepository)
    country_repository = Singleton(CountryRepository)
    visited_repository = Singleton(VisitedRepository)
    favourite_repository = Singleton(FavouriteRepository)


    continent_service = Factory(
        ContinentService,
        repository=continent_repository,
    )
    user_service = Factory(
        UserService,
        repository=user_repository,
    )
    country_service = Factory(
        CountryService,
        repository=country_repository,
    )
    visited_service = Factory(
        VisitedService,
        repository=visited_repository,
    )
    favourite_service = Factory(
        FavouriteService,
        repository=favourite_repository,
    )