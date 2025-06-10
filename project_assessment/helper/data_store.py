import json
from typing import List
from pathlib import Path
from project_assessment.helper.data_model import Node

def save_tree(nodes: List[Node], path: str | Path) -> None:
    """Save the tree to a JSON file."""
    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump([n.to_dict() for n in nodes], f, indent=2)

def load_tree(path: str | Path) -> List[Node]:
    """Load the tree from a JSON file."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return [Node.from_dict(n) for n in json.load(f)]
    