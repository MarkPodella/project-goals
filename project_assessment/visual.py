# sections/visual.py
import json
import streamlit as st

from state_utils import get_nodes
from visualization.visualizer import build_network, render_network
from visualization.visualizer3d import build_plotly_3d     # 3-D-Version
from project_assessment.helper.data_model import Node

# Status-Farben (konsistent mit editor.py und drilldown.py)
STATUS_COLORS = {
    "red":  "#e74c3c",
    "yellow": "#f1c40f",
    "green": "#2ecc71",
}

def render():
    nodes = get_nodes()

    if not nodes:
        st.info("No goal tree yet – please create or load a tree in the 'Goals' tab.")
        return

    st.subheader("🌳 Visualization")

    # ── 1) Optionen
    col_view, _ = st.columns([1, 4])
    view_3d = col_view.checkbox("Enable 3-D view")

    # ── 2) Netzwerk-Graph bauen
    g = build_network(nodes)
    parent_ids = [n.id for n in nodes if any(ch.parent == n.id for ch in nodes)]

    # ── 3) Rendern
    if view_3d:
        fig = build_plotly_3d(g, parent_ids)
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": True,
                "toImageButtonOptions": {
                    "format": "png",
                    "filename": "project_tree_3d",
                    "height": 600,
                    "width": 800,
                    "scale": 1,
                },
            },
        )
    else:
        net = render_network(g)
        html = net.generate_html(notebook=False)
        st.components.v1.html(html, height=650, scrolling=True)
        