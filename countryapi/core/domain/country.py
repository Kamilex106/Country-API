"""Module containing country-related domain models"""
from pydantic import UUID4, BaseModel, ConfigDict


class CountryIn(BaseModel):
    """Model representing country's DTO attributes."""
    name: str
    inhabitants: int
    language: str
    area: int
    pkb: int
    continent_id: int


class CountryBroker(CountryIn):
    """A broker class including user in the model."""
    user_id: UUID4

class Country(CountryBroker):
    """Model representing countries attributes in the database."""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
