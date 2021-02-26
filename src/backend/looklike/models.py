from dataclasses import dataclass
from typing import Optional


@dataclass
class Clothes:
    id: Optional[int]
    name: Optional[str]
    image_path: Optional[str]
    parent_id: Optional[int]
    parent_path: Optional[str]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f'<Clothes id={self.id} Name={self.name}>'

    def __repr__(self):
        return f'<Clothes id={self.id} Name={self.name}>'
