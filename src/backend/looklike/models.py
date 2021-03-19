from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel, validator

from looklike.utils import datetime_to_timestamp


@dataclass
class Clothes:
    id: int
    name: str
    image_path: str
    parent_id: int
    parent_path: str

    def __str__(self):
        return f'<Clothes id={self.id} Name={self.name}>'

    def __repr__(self):
        return f'<Clothes id={self.id} Name={self.name}>'


@dataclass
class Character:
    id: int
    author_id: int
    image_path: str
    description: str
    posted_at: datetime
    clothes: list = field(default_factory=list)

    def __str__(self):
        return f'<Character id={self.id} Description={self.description}>'

    def __repr__(self):
        return f'<Character id={self.id} Description={self.description}>'


class User(BaseModel):
    id: int
    username: str
    password_hash: str
    registered_at: datetime

    class Config:
        json_encoders = {
            datetime: datetime_to_timestamp
        }


class UserLogin(BaseModel):
    username: str
    password: str


class UserRegistration(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, v):
        if not v.isalnum():
            raise ValueError('must be alphanumeric')

        if len(v) > 30 or len(v) < 3:
            raise ValueError('must be more than 3 but less than 30 characters')

        return v

    @validator('password')
    def password_validator(cls, v):
        if len(v) < 8:
            raise ValueError('must contain at least 8 characters')

        number_of_capitals = sum(character.isupper() for character in v)

        if number_of_capitals < 2:
            raise ValueError('must contain at least 2 capital letters')

        number_of_digits = sum(character.isdigit() for character in v)

        if number_of_digits < 3:
            raise ValueError('must contain at least 3 digits')

        return v
