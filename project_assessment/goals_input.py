# project_assessment/goals_input.py
import streamlit as st
import tempfile, os, json
from uuid import uuid4

from project_assessment.helper.tree_builder import build_tree
from project_assessment.helper.data_store import load_tree
from project_assessment.helper.data_model import Node, STATUS_CHOICES
from state_utils import get_nodes, set_nodes, analysis_done

def dict_to_node(node_dict):
    """Convert dictionary to Node object"""
    return Node(
        id=node_dict["id"],
        name=node_dict["name"],
        parent=node_dict.get("parent"),
        status=node_dict.get("status", "yellow"),
        comment=node_dict.get("comment", "")
    )

def node_to_dict(node):
    """Convert Node object to dictionary"""
    return {
        "id": node.id,
        "name": node.name,
        "parent": node.parent,
        "status": node.status,
        "comment": node.comment
    }

# ── Haupt-Render-Funktion (wird von app.py aufgerufen)
def render():
    if "json_loaded" not in st.session_state:
        st.session_state["json_loaded"] = False

    st.subheader("🏗️  Project Goals")
    # Persist goals input across navigation
    goals_input = st.text_area(
        "Enter your goals line by line:",
        value=st.session_state.get("goals_input", ""),
        placeholder="New CRM implementation\nOptimize onboarding process",
        height=120,
        key="goals_input",
    )

    col1, col2, col3 = st.columns(3)

    # -- 1) Baum erzeugen
    with col1:
        if st.button("Create Project Network"):
            if not goals_input.strip():
                st.warning("Please enter at least one goal.")
            else:
                goals = [g.strip() for g in goals_input.splitlines() if g.strip()]
                nodes = build_tree(goals)
                # Convert to dictionaries before storing
                nodes_dict = [node_to_dict(n) for n in nodes]
                set_nodes(nodes)
                # Store the dictionary version in session state for the editor
                st.session_state["editor_nodes"] = nodes_dict
                analysis_done(False)          # Analyse-Flag zurücksetzen
                st.rerun()
                st.success("Project Network created!")

    # -- 2) JSON laden
    with col2:
        uploaded = st.file_uploader("Load from JSON", type=["json"], key="json_uploader")
        if uploaded:
            # only load and rerun once per upload
            if not st.session_state["json_loaded"]:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
                    tmp.write(uploaded.read())
                    tmp_path = tmp.name
                nodes = load_tree(tmp_path)
                set_nodes(nodes)
                # Store the dictionary version in session state for the editor
                st.session_state["editor_nodes"] = [node_to_dict(n) for n in nodes]
                os.unlink(tmp_path)
                analysis_done(False)
                st.session_state["json_loaded"] = True
                st.rerun()
            else:
                st.success("Project Network loaded from JSON!")
        else:
            # reset flag when uploader is cleared
            st.session_state["json_loaded"] = False

    # -- 3) Analyse ausführen
    with col3:
        if st.button("Run Analysis"):
            if not get_nodes():
                st.warning("Please create or load a Project Network first.")
            else:
                analysis_done(True)
                st.success("Analysis started – switch to the *Analysis* tab.")