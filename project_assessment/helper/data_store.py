import json
from typing import List
from project_assessment.helper.data_model import Node

def save_tree(nodes: List[Node], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump([n.to_dict() for n in nodes], f, ensure_ascii=False, indent=2)

def load_tree(path: str) -> List[Node]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Node.from_dict(d) for d in data]