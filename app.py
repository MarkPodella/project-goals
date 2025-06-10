# app.py
import streamlit as st
from sidebar.menu import render_sidebar
from state_utils import get_nodes        # stellt sicher, dass State existiert

st.set_page_config(page_title="Project Goals App", layout="wide")

if "ingested_texts" not in st.session_state:
    st.session_state["ingested_texts"] = {}

from project_assessment.gui import render_assessment

# ── Session-State sicherstellen (erzeugt leeres [] bei erstem Aufruf)
get_nodes()

st.title("🎯 Project Goals App")

render_sidebar(None)
mode = st.session_state.get("workflow_mode")

if mode == "Project Assessment":
    render_assessment()
else:
    st.info("Unknown mode.")