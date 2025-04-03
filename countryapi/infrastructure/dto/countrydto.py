"""A module containing DTO models for output countries."""
from asyncpg import Record  # type: ignore
from pydantic import UUID4, BaseModel, ConfigDict

from countryapi.infrastructure.dto.continentdto import ContinentDTO


class CountryDTO(BaseModel):
    """A model representing DTO for country data."""
    id: int
    name: str
    inhabitants: int
    language: str
    area: int
    pkb: int
    continent: ContinentDTO
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CountryDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            CountryDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            inhabitants=record_dict.get("inhabitants"),  # type: ignore
            language=record_dict.get("language"),  # type: ignore
            area=record_dict.get("area"),  # type: ignore
            pkb=record_dict.get("pkb"),  # type: ignore
            continent=ContinentDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1"),
                alias=record_dict.get("alias"),
            ),
            user_id=record_dict.get("user_id"),

        )