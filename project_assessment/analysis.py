# sections/analysis.py
import streamlit as st

from state_utils import get_nodes, analysis_done
from project_assessment.helper.analysis import (
    aggregate_status,
    compute_metrics,
    critical_paths,
)
from project_assessment.helper.summarizer import generate_summary
from project_assessment.helper.recommendations import load_rules, get_recommendations

def render():
    # Prüfen, ob der Nutzer die Analyse überhaupt aktiviert hat
    if not analysis_done():
        st.info('Analysis not yet performed – go to the "Goals" tab and click **Run analysis**.')
        return

    nodes = get_nodes()
    if not nodes:
        st.warning("No goal tree available.")
        return

    # ── 1) Status zusammen­fassen (Sicherheitshalber)
    aggregate_status(nodes)

    # ── 2) KPI-Dashboard
    st.subheader("📊 Key Metrics")
    m = compute_metrics(nodes)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Red",  f'{m["red"]}/{m["total"]}',  f'{m["red_pct"]*100:.0f}%')
    c2.metric("Yellow", f'{m["yellow"]}/{m["total"]}', f'{m["yellow_pct"]*100:.0f}%')
    c3.metric("Green", f'{m["green"]}/{m["total"]}', f'{m["green_pct"]*100:.0f}%')
    c4.metric("Total", m["total"])

    # ── 3) Kritische Pfade
    st.subheader("🔥 Critical Paths")
    for p in critical_paths(nodes):
        # Alle bis auf das letzte Element fett
        formatted = [f"**{name}**" for name in p[:-1]] + [p[-1]]
        st.markdown(" → ".join(formatted))

    # ── 4) Zusammenfassung
    st.subheader("✍️ Summary")
    st.markdown(generate_summary(nodes))

    # ── 5) Empfehlungen
    st.subheader("💡 Recommendations")
    recs = get_recommendations(nodes, load_rules())
    if recs:
        for r in recs:
            st.markdown(f"- {r}")
    else:
        st.info("No recommendations based on current rules.")