from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import List, Optional


class AuthorSchema(BaseModel):
    author: str = Field(..., min_length=3, max_length=140)


class AuthorDB(AuthorSchema):
    id: int

class StatusEnum(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"

class NewBookSchema(BaseModel):
    title: str = Field(...,min_length=3,max_length=140)
    year: int = Field(..., ge=0)
    status: StatusEnum = Field(StatusEnum.DRAFT, description="The status of the book")
    author_id: Optional[int] = Field(None)
    author_name: Optional[str] = Field(None)

    @validator("author_name")
    def validate_author_name(cls, value):
        if value == "" or value is None:
            return value
        if not (3 <= len(value) <= 140):
            raise ValueError("Author name must be between 3 and 140 characters.")
        return value

# Base schema with common fields
class BookSchema(BaseModel):
    title: str = Field(...,min_length=3,max_length=140)
    year: int = Field(..., ge=0)
    status: StatusEnum = Field(StatusEnum.DRAFT, description="The status of the book")
    author: int = Field(...)

class BookDB(BookSchema):
    id: int

class GetAllSchema(BaseModel):
    authors: List[AuthorDB]
    books: List[BookDB]

