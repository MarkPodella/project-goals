# sections/editor.py
import json, streamlit as st
import pandas as pd
from uuid import uuid4
from pathlib import Path
import yaml

from project_assessment.helper.data_model import STATUS_CHOICES, Node
from state_utils import get_nodes, set_nodes

def dict_to_node(node_dict):
    """Convert dictionary to Node object"""
    return Node(
        id=node_dict["id"],
        name=node_dict["name"],
        parent=node_dict.get("parent"),
        status=node_dict.get("status", "yellow"),  # Default status is "yellow"
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

def get_children(parent_id, nodes_dict):
    """Get all children of a parent node"""
    return [n for n in nodes_dict if n.get("parent") == parent_id]

def get_node_by_id(node_id, nodes_dict):
    """Get node by ID"""
    return next((n for n in nodes_dict if n["id"] == node_id), None)

def load_questions():
    """Load questions from YAML file"""
    questions_path = Path("config/questions.yaml")
    if questions_path.exists():
        try:
            with questions_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            st.error(f"Error loading questions: {e}")
    return {}

# ── Haupt-Render-Funktion
def render():
    # Get nodes from session state if available, otherwise from state_utils
    if "editor_nodes" in st.session_state:
        nodes_dict = st.session_state["editor_nodes"]
    else:
        nodes = get_nodes()
        nodes_dict = [node_to_dict(n) for n in nodes]

    # 1) Hinweis, falls noch kein Baum existiert
    if not nodes_dict:
        st.info("No goal tree yet – please enter goals first.")
        return

    st.subheader("📝 Goal Editor")

    # 2) Hauptziele (Nodes ohne Parent)
    st.subheader("Main Goals:")
    root_nodes = [n for n in nodes_dict if n.get("parent") is None]
    
    for node in root_nodes:
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            status = node.get("status", "yellow")
            farbe = {"red": "red", "yellow": "orange", "green": "green"}.get(status, "gray")
            st.markdown(f'<span style="color:{farbe}">●</span> **{node["name"]}**  \n_Status: {status}_', unsafe_allow_html=True)
        with col2:
            if st.button("Edit", key=f"edit_{node['id']}"):
                st.session_state.active_node_id = node["id"]
                st.rerun()
        with col3:
            if st.button("🗑️", key=f"delete_{node['id']}"):
                nodes_dict = [n for n in nodes_dict if n["id"] != node["id"]]
                st.session_state["editor_nodes"] = nodes_dict
                updated_nodes = [dict_to_node(n) for n in nodes_dict]
                set_nodes(updated_nodes)
                st.rerun()

    # 3) Neues Hauptziel hinzufügen
    with st.form("add_root_goal"):
        new_name = st.text_input("Enter new main goal:")
        if st.form_submit_button("Add") and new_name:
            new_node = {
                "id": str(uuid4()),
                "parent": None,
                "name": new_name,
                "status": "yellow",
                "comment": ""
            }
            nodes_dict.append(new_node)
            st.session_state["editor_nodes"] = nodes_dict
            updated_nodes = [dict_to_node(n) for n in nodes_dict]
            set_nodes(updated_nodes)
            st.rerun()

    # 4) Aktiver Knoten bearbeiten
    if "active_node_id" not in st.session_state:
        st.session_state.active_node_id = None

    if st.session_state.active_node_id:
        current_node = get_node_by_id(st.session_state.active_node_id, nodes_dict)
        if current_node:
            st.markdown("---")
            st.markdown(f"**Editing:** {current_node['name']}")

            with st.form("edit_node"):
                name = st.text_input("Title", value=current_node.get("name", ""))
                comment = st.text_area("Comment", value=current_node.get("comment", ""))
                status = st.selectbox("Status", 
                                    ["red", "yellow", "green"],
                                    index=["red", "yellow", "green"].index(current_node.get("status", "yellow")))
                
                if st.form_submit_button("Save"):
                    current_node["name"] = name
                    current_node["comment"] = comment
                    current_node["status"] = status
                    st.session_state["editor_nodes"] = nodes_dict
                    updated_nodes = [dict_to_node(n) for n in nodes_dict]
                    set_nodes(updated_nodes)
                    st.success("Goal updated")
                    st.rerun()

            # Unterziele anzeigen
            st.subheader("Subgoals:")
            children = get_children(current_node["id"], nodes_dict)
            
            for child in children:
                col1, col2, col3 = st.columns([5, 1, 1])
                with col1:
                    status = child.get("status", "yellow")
                    farbe = {"red": "red", "yellow": "orange", "green": "green"}.get(status, "gray")
                    st.markdown(f'<span style="color:{farbe}">●</span> **{child["name"]}**  \n_Status: {status}_', unsafe_allow_html=True)
                with col2:
                    if st.button("Edit", key=f"edit_{child['id']}"):
                        st.session_state.active_node_id = child["id"]
                        st.rerun()
                with col3:
                    if st.button("🗑️", key=f"delete_{child['id']}"):
                        nodes_dict = [n for n in nodes_dict if n["id"] != child["id"]]
                        st.session_state["editor_nodes"] = nodes_dict
                        updated_nodes = [dict_to_node(n) for n in nodes_dict]
                        set_nodes(updated_nodes)
                        st.rerun()

            # Neues Unterziel hinzufügen
            with st.form("add_child"):
                new_name = st.text_input("Enter new subgoal:")
                if st.form_submit_button("Add") and new_name:
                    new_node = {
                        "id": str(uuid4()),
                        "parent": current_node["id"],
                        "name": new_name,
                        "status": "yellow",
                        "comment": ""
                    }
                    nodes_dict.append(new_node)
                    st.session_state["editor_nodes"] = nodes_dict
                    updated_nodes = [dict_to_node(n) for n in nodes_dict]
                    set_nodes(updated_nodes)
                    st.rerun()

            # Zurück-Button
            if st.button("← Back to overview"):
                st.session_state.active_node_id = None
                st.rerun()

    # 5) Download JSON
    json_data = json.dumps(nodes_dict, ensure_ascii=False, indent=2)
    st.download_button(
        "💾 Save project as JSON",
        json_data,
        file_name="project_network.json",
        mime="application/json",
    )
    