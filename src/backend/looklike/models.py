from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple, Optional


class Clothes(NamedTuple):
    id: Optional[int]
    name: Optional[str]
    image_path: Optional[str]
    parent_id: Optional[int]
    parent_path: Optional[str]

    def __str__(self):
        return f'<Clothes id={self.id} Name={self.name}>'

    def __repr__(self):
        return f'<Clothes id={self.id} Name={self.name}>'


@dataclass
class Character:
    id: Optional[int]
    author_id: Optional[int]
    image_path: Optional[str]
    description: Optional[str]
    posted_at: Optional[datetime]
    clothes: Optional[list]

    def __init__(self, *args, **kwargs):
        self.clothes = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f'<Character id={self.id} Description={self.description}>'

    def __repr__(self):
        return f'<Character id={self.id} Description={self.description}>'
