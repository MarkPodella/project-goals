import json
import re
from typing import List, Dict
from pathlib import Path
import yaml
from project_assessment.helper.data_model import Node

def load_rules(path: str = "config/rules.yaml") -> List[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        return []

def get_recommendations(nodes: List[Node], rules: List[dict]) -> List[str]:
    recs = []
    for n in nodes:
        for rule in rules:
            pattern = rule.get("match", "")
            if pattern and re.search(pattern, n.name, re.I) and n.status == "red":
                recs.append(f"**{n.name}** → {rule.get('action')}")
    return recs

def load_recommendations(path: str | Path) -> Dict[str, List[str]]:
    """Load recommendations from a JSON file."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
    