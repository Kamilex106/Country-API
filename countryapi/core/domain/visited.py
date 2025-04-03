"""Module containing visited-related domain models."""
from pydantic import BaseModel, ConfigDict, UUID4


class VisitedIn(BaseModel):
    """Model representing visited DTO attributes."""
    country_name: str

class VisitedBroker(VisitedIn):
    """A broker class including user in the model."""
    user_id: UUID4

class Visited(VisitedIn):
    """Model representing visited attributes in the database."""
    id: int
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True, extra="ignore")


