from __future__ import annotations

from datetime import datetime
from typing import Self
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class FilmBase(BaseModel):
    """Base schema holding common film attributes."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    title: str = Field(min_length=1, description="Title of the film (cannot be empty)")
    release_year: int = Field(description="Year the film was released (must be an integer)")
    genre: str = Field(min_length=1, description="Genre of the film (e.g. Sci-Fi, Action)")
    director: str = Field(min_length=1, description="Full name of the film director")


class FilmCreate(FilmBase):
    """
    Schema for creating a new film.
    Inherits all common fields from FilmBase.
    """
    pass


class FilmResponse(FilmBase):
    """
    Schema returned to the client when a film is created or retrieved.
    Inherits title, release_year, genre, and director from FilmBase,
    and adds the database id and a computed 'years_ago' field.
    """
    id: int = Field(description="Unique identifier of the film")

    @computed_field
    @property
    def years_ago(self) -> int:
        """
        Computes how many years ago the film was released
        relative to the current year.
        """
        current_calendar_year = datetime.now().year
        return current_calendar_year - self.release_year


class ReleaseWindow(BaseModel):
    """
    Schema demonstrating cross-field validation with @model_validator.
    Ensures start_year <= end_year.
    """
    model_config = ConfigDict(strict=True)

    start_year: int = Field(description="Starting year of the release window")
    end_year: int = Field(description="Ending year of the release window")

    @model_validator(mode="before")
    def validate_release_year_range(self) -> Self:
        """
        Validates that the starting year is not greater than the ending year.
        """
        if self.start_year > self.end_year:
            raise ValueError("start_year must be less than or equal to end_year")
        return self


class FilmUpdate(BaseModel):
    """Schema for updating an existing film."""
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)

    title: str | None = None
    release_year: int | None = None
    genre: str | None = None
    director: str | None = None


class FilmPlaceholderResponse(BaseModel):
    """Placeholder response for film details."""
    model_config = ConfigDict(strict=True)

    message: str
    film_id: int


class FilmListPlaceholderResponse(BaseModel):
    """Placeholder response for film lists."""
    model_config = ConfigDict(strict=True)

    message: str
    genre: str | None = None
