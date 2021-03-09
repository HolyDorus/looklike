from dataclasses import dataclass, field
from datetime import datetime


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
