"""A module containing DTO models for output continents."""
from pydantic import BaseModel, ConfigDict  # type: ignore

class ContinentDTO(BaseModel):
    """A model representing DTO for continent data."""
    id: int
    name: str
    alias: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
