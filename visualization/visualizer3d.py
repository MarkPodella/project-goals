"""
visualizer3d.py
----------------
3‑D visualization of the project tree using Plotly.

• Parent nodes as larger, colored markers based on traffic light status.
• Child nodes as smaller, gray markers.
• Edges as lines.
"""

import networkx as nx
import plotly.graph_objects as go
from typing import List, Union, Dict

from project_assessment.helper.data_model import Node

# Status colors (traffic light style in HEX)
STATUS_COLORS = {
    "red":  "#e74c3c",
    "yellow": "#f1c40f",
    "green": "#2ecc71",
}

def dict_to_node(node_dict: Dict) -> Node:
    """Convert dictionary to Node object"""
    return Node(
        id=node_dict["id"],
        name=node_dict["name"],
        parent=node_dict.get("parent"),
        status=node_dict.get("status", "yellow"),
        comment=node_dict.get("comment", "")
    )

def build_plotly_3d(g: nx.DiGraph, parent_ids: List[str]) -> go.Figure:
    """
    Creates a 3-D Plotly figure from the NetworkX graph.

    Parameters
    ----------
    g : nx.DiGraph
        The graph with node attributes 'label' and 'color'.
        'color' can be a HEX string or a dict like {'border': ...}.
    parent_ids : List[str]
        IDs of parent nodes.

    Returns
    -------
    go.Figure
    """
    # 1) Position layout in 3D
    pos = nx.spring_layout(g, dim=3, seed=42)

    # 2) Edges as lines
    edge_x, edge_y, edge_z = [], [], []
    for u, v in g.edges():
        x0, y0, z0 = pos[u]
        x1, y1, z1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_z += [z0, z1, None]

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode="lines",
        line=dict(width=2, color="#888"),
        hoverinfo="none"
    )

    # 3) Nodes with text and color
    node_x, node_y, node_z = [], [], []
    node_text, node_color, node_size = [], [], []

    for node_id in g.nodes():
        x, y, z = pos[node_id]
        node_x.append(x); node_y.append(y); node_z.append(z)
        node_text.append(g.nodes[node_id].get("label", ""))

        # Extract base color
        raw_color = g.nodes[node_id].get("color", "#888888")
        # If a dict is used (e.g. pyvis fallback), take .border
        if isinstance(raw_color, dict):
            col = raw_color.get("border", "#888888")
        else:
            col = raw_color

        if node_id in parent_ids:
            node_color.append(col)
            node_size.append(12)
        else:
            node_color.append("#888888")
            node_size.append(6)

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode="markers+text",
        marker=dict(size=node_size, color=node_color),
        text=node_text,
        textposition="bottom center",
        hoverinfo="text"
    )

    # Final layout
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        )
    )
    return fig
