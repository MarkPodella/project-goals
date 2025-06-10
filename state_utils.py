# state_utils.py
import streamlit as st
from typing import List
from project_assessment.helper.data_model import Node

def get_nodes() -> List[Node]:
    """Garantiert ein Knoten-Array im Session-State und gibt es zurück."""
    if "nodes" not in st.session_state:
        st.session_state["nodes"] = []
    return st.session_state["nodes"]

def set_nodes(nodes: List[Node]) -> None:
    """Schreibt das Knoten-Array zurück in den Session-State."""
    st.session_state["nodes"] = nodes

def analysis_done(flag: bool | None = None) -> bool:
    """
    Getter/Setter für das Analyse-Flag.
    - Ohne Argument: aktuellen Zustand lesen.
    - Mit Argument: neuen Zustand setzen.
    """
    if flag is None:
        return st.session_state.get("analysis_done", False)
    st.session_state["analysis_done"] = flag
    return flag
