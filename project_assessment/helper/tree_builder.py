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

from typing import List, Dict, Any
from pathlib import Path
import yaml

from project_assessment.helper.data_model import Node


# --------------------------------------------------------------------------- #
# 1.  Fragenkatalog laden
# --------------------------------------------------------------------------- #
# YAML‑Pfad – bei Bedarf anpassen
QUESTIONS_YAML = Path("config/questions.yaml")

# Minimal‑Fallback (keine Fragen), falls YAML fehlt/unkorrekt
FALLBACK_QUESTIONS: dict[str, list[str]] = {
    "Prozess": [],
    "System": [],
    "Mensch": [],
}


def process_yaml_node(node: Any, parent_id: str, nodes: List[Node], level: int = 0) -> None:
    """
    Process a YAML node recursively to build the tree structure.
    
    Parameters
    ----------
    node : Any
        The current YAML node to process
    parent_id : str
        The ID of the parent node
    nodes : List[Node]
        The list of nodes to append to
    level : int
        The current indentation level
    """
    if isinstance(node, dict):
        for key, value in node.items():
            # Create a node for the key
            key_node = Node(name=key, parent=parent_id)
            nodes.append(key_node)
            # Process the value recursively
            process_yaml_node(value, key_node.id, nodes, level + 1)
    elif isinstance(node, list):
        current_parent = parent_id
        for item in node:
            if isinstance(item, str):
                # Create a leaf node
                nodes.append(Node(name=item, parent=current_parent))
            else:
                # Process nested structures
                process_yaml_node(item, current_parent, nodes, level + 1)
    elif isinstance(node, str):
        # Create a leaf node
        nodes.append(Node(name=node, parent=parent_id))


def load_questions(path: Path = QUESTIONS_YAML) -> List[Node]:
    """
    Versucht, die Achsen/Fragen aus der YAML zu laden.
    Gibt bei Fehlern das Fallback‑Gerüst zurück.
    """
    if path.exists():
        try:
            # Read the YAML file as text to preserve indentation
            yaml_text = path.read_text(encoding="utf-8")
            # Split into lines and process indentation
            lines = yaml_text.split('\n')
            nodes = []
            stack = [(None, -1)]  # (parent_id, indentation_level)
            
            for line in lines:
                if not line.strip():
                    continue
                    
                # Count leading spaces to determine indentation level
                indent = len(line) - len(line.lstrip())
                content = line.strip()
                
                # Skip empty lines and comments
                if not content or content.startswith('#'):
                    continue
                    
                # Remove list markers
                if content.startswith('- '):
                    content = content[2:]
                
                # Pop stack until we find the appropriate parent
                while stack and stack[-1][1] >= indent:
                    stack.pop()
                
                # Create new node
                parent_id = stack[-1][0]
                node = Node(name=content, parent=parent_id)
                nodes.append(node)
                
                # Push this node onto the stack
                stack.append((node.id, indent))
            
            return nodes
        except yaml.YAMLError as err:
            print(f"[WARN] YAML‑Parse‑Fehler in {path}: {err}")
    else:
        print(f"[INFO] {path} nicht gefunden – nutze Fallback‑Fragen.")

    # Return fallback structure
    nodes = []
    for category in FALLBACK_QUESTIONS:
        node = Node(name=category)
        nodes.append(node)
    return nodes


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
     ├─ Achse (z. B. 'Prozess')
     │   ├─ Frage 1
     │   ├─ Frage 2
     │   └─ ...
     └─ ...
    """
    nodes: list[Node] = []

    for raw_goal in goals:
        goal = raw_goal.strip()
        if not goal:
            continue

        # Wurzelknoten = Projektziel
        root = Node(name=goal)
        nodes.append(root)

        # Load and process the YAML structure
        yaml_nodes = load_questions()
        for node in yaml_nodes:
            if node.parent is None:  # Top-level nodes
                node.parent = root.id
            nodes.append(node)

    return nodes
