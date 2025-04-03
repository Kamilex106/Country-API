"""Module containing favourite-related domain models."""
from pydantic import BaseModel, ConfigDict, UUID4


class FavouriteIn(BaseModel):
    """Model representing favourites DTO attributes."""
    country_name: str

class FavouriteBroker(FavouriteIn):
    """A broker class including user in the model."""
    user_id: UUID4

class Favourite(FavouriteIn):
    """Model representing favourites attributes in the database."""
    id: int
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True, extra="ignore")


