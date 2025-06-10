import streamlit as st

def render_sidebar(mode):

    # Workflow header
    st.sidebar.title("Workflow")
    st.sidebar.radio("Choose your scenario", [
        "Project Assessment"
    ], key="workflow_mode")
