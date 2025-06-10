"""
visualizer.py
-------------
2‑D visualization of the project tree using pyvis.

• Parent nodes (nodes with children) are highlighted by:
    – bold text
    – colored border (traffic light status)
    – thick border width
    – ellipse shape

• Child nodes (questions) appear as plain text (shape="text"),
  with no border and normal font weight.
"""

import networkx as nx
from pyvis.network import Network
from collections import Counter
from typing import List, Union, Dict

from project_assessment.helper.data_model import Node

# Status colors (traffic light style)
STATUS_COLORS = {
    "red":  "#e74c3c",
    "yellow": "#f1c40f",
    "green": "#2ecc71",
}

def dict_to_node(node_dict: Union[Dict, Node]) -> Node:
    """Convert dictionary or Node to Node object"""
    if isinstance(node_dict, Node):
        return node_dict
    return Node(
        id=node_dict["id"],
        name=node_dict["name"],
        parent=node_dict.get("parent"),
        status=node_dict.get("status", "yellow"),
        comment=node_dict.get("comment", "")
    )

def build_network(nodes: List[Union[Node, Dict]]) -> nx.DiGraph:
    """Builds a NetworkX graph with visualization attributes."""
    # Convert dictionaries to Node objects if needed
    node_objects = [n if isinstance(n, Node) else dict_to_node(n) for n in nodes]
    
    g = nx.DiGraph()
    # Count which nodes have at least one child
    child_cnt = Counter(n.parent for n in node_objects if n.parent)

    for n in node_objects:
        is_parent = child_cnt.get(n.id, 0) > 0

        if is_parent:
            # Parents: ellipse with border and bold label
            g.add_node(
                n.id,
                label=n.name,
                title=f"{n.name}<br>Status: {n.status}<br>Comment: {n.comment}",
                shape="ellipse",
                font={"bold": True},
                borderWidth=3,
                color={
                    "border": STATUS_COLORS.get(n.status, "#888888"),
                    "background": "#ffffff",
                    "highlight": {
                        "border": STATUS_COLORS.get(n.status, "#888888"),
                        "background": "#ffffff"
                    }
                },
            )
        else:
            # Children: plain text, no border
            g.add_node(
                n.id,
                label=n.name,
                title=f"{n.name}<br>Status: {n.status}<br>Comment: {n.comment}",
                shape="text",
                font={"bold": False},
            )

    # Add edges
    for n in node_objects:
        if n.parent:
            g.add_edge(n.parent, n.id)

    return g

def render_network(g: nx.DiGraph, height: str = "650px", width: str = "100%") -> Network:
    """Converts the NetworkX graph to a pyvis.Network."""
    net = Network(height=height, width=width, directed=True)
    net.from_nx(g)
    net.repulsion(node_distance=150, spring_length=200)
    return net