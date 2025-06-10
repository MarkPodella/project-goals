from typing import List
from project_assessment.helper.data_model import Node

def generate_summary(nodes: List[Node]) -> str:
    """
    Erstellt eine Zusammenfassung:
    - Listet rote und gelbe Knoten auf.
    - Fettet alle Parent-Knoten (Ziele und Achsen).
    """
    # 1) Ermittel alle Parent-IDs (haben mindestens ein Kind)
    parent_ids = {n.id for n in nodes if any(m.parent == n.id for m in nodes)}

    # 2) Sammle Labels, fett bei Parent
    reds, yellows = [], []
    for n in nodes:
        label = f"**{n.name}**" if n.id in parent_ids else n.name
        if n.status == "red":
            reds.append(label)
        elif n.status == "yellow":
            yellows.append(label)

    # 3) Baue Markdown-Zusammenfassung
    lines = ["**Current main problems (Red):**"]
    if reds:
        lines.extend(f"- {r}" for r in reds)
    else:
        lines.append("- No red nodes.")

    lines.append("")  # Leerzeile zwischen Abschnitten
    lines.append("**Observation points (Yellow):**")
    if yellows:
        lines.extend(f"- {y}" for y in yellows)
    else:
        lines.append("- No yellow nodes.")

    return "\n".join(lines)
