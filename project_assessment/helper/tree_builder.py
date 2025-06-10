"""
tree_builder.py
----------------
Erzeugt für jedes eingegebene Projektziel einen hierarchischen Baum
(Ziel  ➜  Achse  ➜  Reflexionsfrage).

• Die Fragen‑ und Achsen‑Definitionen werden primär aus
  'config/questions.yaml' geladen.

• Fehlt die YAML oder ist defekt, greift ein minimalistisches Fallback‑Gerüst
  (Achsen ohne Fragen), damit die App nicht abstürzt.
"""

from __future__ import annotations

from typing import List
from pathlib import Path
import yaml

from project_assessment.helper.data_model import Node


# --------------------------------------------------------------------------- #
# 1.  Fragenkatalog laden
# --------------------------------------------------------------------------- #
# YAML‑Pfad – bei Bedarf anpassen
QUESTIONS_YAML = Path("config/questions.yaml")

# Minimal‑Fallback (keine Fragen), falls YAML fehlt/unkorrekt
FALLBACK_QUESTIONS: dict[str, list[str]] = {
    "Prozess": [],
    "System": [],
    "Mensch": [],
}


def load_questions(path: Path = QUESTIONS_YAML) -> dict[str, list[str]]:
    """
    Versucht, die Achsen/Fragen aus der YAML zu laden.
    Gibt bei Fehlern das Fallback‑Gerüst zurück.
    """
    if path.exists():
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            # Plausibilitätscheck: alles Listen?
            if all(isinstance(v, list) for v in data.values()):
                return data
            else:
                print("[WARN] questions.yaml: Mindestens ein Wert ist keine Liste.")
        except yaml.YAMLError as err:
            print(f"[WARN] YAML‑Parse‑Fehler in {path}: {err}")
    else:
        print(f"[INFO] {path} nicht gefunden – nutze Fallback‑Fragen.")

    return FALLBACK_QUESTIONS


# 2.  Öffentliche API
# --------------------------------------------------------------------------- #
def build_tree(goals: List[str]) -> List[Node]:
    """
    Baut die Node‑Liste für alle übergebenen Projektziele.

    Parameters
    ----------
    goals : List[str]
        Eine Liste von Projektzielen (leer/Whitespace wird ignoriert).

    Returns
    -------
    List[Node]
        Flache Liste aller erzeugten Knoten (Ziele, Achsen, Fragen).

    Struktur
    --------
    Wurzel (Ziel)
     ├─ Achse (z. B. 'Prozess')
     │   ├─ Frage 1
     │   ├─ Frage 2
     │   └─ ...
     └─ ...
    """
    questions_catalog = load_questions()
    nodes: list[Node] = []

    for raw_goal in goals:
        goal = raw_goal.strip()
        if not goal:
            continue

        # Wurzelknoten = Projektziel
        root = Node(name=goal)
        nodes.append(root)

        # Achsen + Fragen
        for axis, questions in questions_catalog.items():
            axis_node = Node(name=axis, parent=root.id)
            nodes.append(axis_node)

            # Jede Frage als Blattknoten
            for q in questions:
                nodes.append(Node(name=q, parent=axis_node.id))

    return nodes