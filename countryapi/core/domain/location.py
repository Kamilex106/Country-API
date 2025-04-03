"""Module containing location-related domain models."""
from pydantic import BaseModel, ConfigDict


class ContinentIn(BaseModel):
    """Model representing continent's DTO attributes."""
    name: str
    alias: str


class Continent(ContinentIn):
    """Model representing continent's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


