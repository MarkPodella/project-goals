import streamlit as st
from project_assessment import editor, goals_input, analysis, visual

def render_assessment():
   # st.title("01 - 🕸️ Project Goals")

    sections = [
        ("📝 Input", goals_input.render),
        ("🗂️ Edit", editor.render),
        ("📊 Analysis", analysis.render),
        ("🌳 Visual", visual.render),
    ]

    for label, render_fn in sections:
        with st.expander(label, expanded=True):
            render_fn()
