"""
Analysefunktionen:
- Ampel-Roll-up
- Kennzahlen
- Kritische Pfade
"""
from typing import List, Dict
from project_assessment.helper.data_model import Node

STATUS_RANK = {"red": 2, "yellow": 1, "green": 0}

def aggregate_status(nodes: List[Node]) -> None:
    """Raise the most critical status of each goal to the root."""
    lookup = {n.id: n for n in nodes}
    changed = True
    while changed:
        changed = False
        for n in nodes:
            if n.parent:
                parent = lookup[n.parent]
                if STATUS_RANK[n.status] > STATUS_RANK[parent.status]:
                    parent.status = n.status
                    changed = True

def compute_metrics(nodes: List[Node]) -> Dict[str, float]:
    total = len(nodes)
    reds = sum(1 for n in nodes if n.status == "red")
    yellows = sum(1 for n in nodes if n.status == "yellow")
    greens = sum(1 for n in nodes if n.status == "green")
    return {
        "total": total,
        "red": reds,
        "yellow": yellows,
        "green": greens,
        "red_pct": reds / total if total else 0,
        "yellow_pct": yellows / total if total else 0,
        "green_pct": greens / total if total else 0,
    }

def critical_paths(nodes: List[Node]):
    """Returns paths (list of names) to all red nodes."""
    lookup = {n.id: n for n in nodes}
    paths = []
    for n in nodes:
        if n.status == "red":
            path = []
            cur = n
            while cur:
                path.append(cur.name)
                cur = lookup.get(cur.parent)
            paths.append(list(reversed(path)))
    return paths