from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4

STATUS_CHOICES = ("red", "yellow", "green")

@dataclass
class Node:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    parent: Optional[str] = None
    status: str = "yellow"
    comment: str = ""

    def __post_init__(self):
        if self.status not in STATUS_CHOICES:
            raise ValueError(f"Status must be one of {STATUS_CHOICES}, got {self.status}")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent": self.parent,
            "status": self.status,
            "comment": self.comment,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    