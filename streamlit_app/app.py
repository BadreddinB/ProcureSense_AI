from pathlib import Path
import sys

import streamlit as st
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.prediction import load_pipeline, load_data, predict_supplier, explain_prediction

st.set_page_config(
    page_title="ProcureSense AI",
    page_icon="🧭",
    layout="wide"
)

# ------------------------------------------------------------
# Design system - CSS
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #F6F4EE;
    --paper: #FFFFFF;
    --border: #E4E0D3;
    --ink: #1E2A24;
    --ink-soft: #5B6960;
    --ink-faint: #8B968D;
    --pine: #35594A;
    --pine-deep: #24402F;
    --pine-tint: #E7EEE7;
    --clay: #BE7A47;
    --clay-tint: #F3E7DA;
    --low: #3E7856;
    --low-tint: #E4EFE6;
    --med: #C08A2E;
    --med-tint: #F5EBD6;
    --high: #B0543C;
    --high-tint: #F5E2DB;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--bg);
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

.block-container {
    max-width: 1100px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    color: var(--ink) !important;
}

h2 {
    font-size: 21px !important;
    margin-bottom: 10px !important;
}

p, span, div, label, li {
    color: var(--ink);
}

/* Card look for st.container(border=True) blocks, applied to the closest
   container carrying a .card-frame marker (see usage below) */
.card-frame { display: none; }

div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .card-frame) {
    background: var(--paper) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    box-shadow: 0 1px 2px rgba(30,42,36,0.04), 0 8px 24px -12px rgba(30,42,36,0.12) !important;
    padding: 20px 22px !important;
}

/* Selectbox — closed state */
div[data-baseweb="select"] > div {
    background: #FBFAF6 !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] * {
    color: var(--ink) !important;
}

/* Selectbox — open dropdown list (rendered outside .stApp, needs its own theming) */
div[data-baseweb="popover"] {
    z-index: 999999 !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] {
    background: var(--paper) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 24px -8px rgba(30,42,36,0.25) !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"] {
    background: transparent !important;
    color: var(--ink) !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"]:hover,
ul[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] {
    background: var(--pine-tint) !important;
    color: var(--pine-deep) !important;
}

hr {
    border-color: var(--border);
}
</style>
""", unsafe_allow_html=True)

pipeline = load_pipeline()
data = load_data()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown("""
<div style="display:flex; align-items:center; gap:16px; padding-bottom:28px;
            border-bottom:1px solid var(--border); margin-bottom:36px;">
    <div style="width:46px;height:46px;border-radius:12px;
                background:linear-gradient(155deg,var(--pine) 0%, var(--pine-deep) 100%);
                display:flex;align-items:center;justify-content:center;flex-shrink:0;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M4 18L9 10L14 14L20 5" stroke="#F3F1E8" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M15 5H20V10" stroke="#F3F1E8" stroke-width="2"
                  stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <h1 style="font-size:32px;margin:0 0 4px;">ProcureSense AI</h1>
        <p style="font-size:15.5px;color:var(--ink-soft);margin:0;">
            Supplier Risk &amp; Performance Intelligence
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Project overview
# ------------------------------------------------------------
st.header("Project overview")
st.write("""
ProcureSense AI transforms procurement data into actionable insights,
helping teams evaluate supplier risk, monitor performance,
and strengthen operational reliability.
""")

st.divider()

# ------------------------------------------------------------
# Supplier risk prediction
# ------------------------------------------------------------
st.header("Supplier risk prediction")
st.markdown(
    '<p style="font-size:13.5px;color:var(--ink-soft);margin-bottom:14px;">'
    'Select a supplier to generate its risk profile</p>',
    unsafe_allow_html=True
)

with st.container(border=True):
    st.markdown('<span class="card-frame"></span>', unsafe_allow_html=True)
    selected_supplier = st.selectbox(
        "Select a supplier",
        options=sorted(data["Supplier"].unique())
    )

supplier_profile = data[data["Supplier"] == selected_supplier].iloc[0]

st.divider()

# ------------------------------------------------------------
# Supplier profile
# ------------------------------------------------------------
total_cost_saving = round(
    supplier_profile["Cost_Saving"] * supplier_profile["Quantity"],
    2
)

st.header("Supplier profile")

with st.container(border=True):
    st.markdown('<span class="card-frame"></span>', unsafe_allow_html=True)
    initial = selected_supplier[:1].upper()
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px;">
        <div style="width:48px;height:48px;border-radius:12px;background:var(--clay-tint);color:var(--clay);
                    display:flex;align-items:center;justify-content:center;font-family:'Fraunces',serif;
                    font-weight:600;font-size:18px;flex-shrink:0;">{initial}</div>
        <div>
            <p style="font-size:17px;font-weight:600;margin:0 0 2px;">{selected_supplier}</p>
            <p style="font-size:13px;color:var(--ink-soft);margin:0;">{supplier_profile['Item_Category']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    profile_items = (
        ("Quantity", f"{int(supplier_profile['Quantity']):,} units"),
        ("Estimated spend", f"{supplier_profile['Estimated_Spend']:,.2f}"),
        ("Total cost saving", f"{total_cost_saving:,.2f}"),
    )
    for col, (label, value) in zip((p1, p2, p3), profile_items):
        col.markdown(f"""
        <div style="padding:14px 16px;background:#FBFAF6;border:1px solid var(--border);border-radius:10px;">
            <p style="font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;
                      color:var(--ink-soft);margin:0 0 6px;">{label}</p>
            <p style="font-size:16px;font-weight:600;margin:0;">{value}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ------------------------------------------------------------
# Procurement KPIs
# ------------------------------------------------------------
compliance_rate = data["Compliance"].mean()

risk_label, risk_score = predict_supplier(pipeline, supplier_profile)


def risk_category(score: float) -> str:
    if score < 0.33:
        return "Low"
    elif score < 0.66:
        return "Medium"
    else:
        return "High"


_badge_class_map = {"Low": "low", "Medium": "med", "High": "high"}
badge_label = risk_category(risk_score)
badge_class = _badge_class_map[badge_label]

st.header("Procurement KPIs")

k1, k2, k3 = st.columns(3)

with k1:
    with st.container(border=True):
        st.markdown('<span class="card-frame"></span>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:12.5px;font-weight:600;color:var(--ink-soft);text-transform:uppercase;'
            'letter-spacing:.05em;margin:0 0 10px;">Overall Supplier Compliance Rate</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<p style="font-family:\'Fraunces\',serif;font-size:32px;font-weight:500;margin:0 0 6px;">'
            f'{compliance_rate * 100:.1f}%</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-size:12.5px;color:var(--ink-faint);margin:0;">'
            'Percentage of purchase orders classified as compliant.</p>',
            unsafe_allow_html=True
        )

with k2:
    with st.container(border=True):
        st.markdown('<span class="card-frame"></span>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:12.5px;font-weight:600;color:var(--ink-soft);text-transform:uppercase;'
            'letter-spacing:.05em;margin:0 0 10px;">Supplier Risk</p>',
            unsafe_allow_html=True
        )
        st.markdown(f"""
        <span style="display:inline-flex;align-items:center;gap:8px;padding:7px 14px;border-radius:999px;
                     font-size:15px;font-weight:600;background:var(--{badge_class}-tint);
                     color:var(--{badge_class});">
            <span style="width:8px;height:8px;border-radius:50%;background:currentColor;"></span>{badge_label}
        </span>
        """, unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:12.5px;color:var(--ink-faint);margin:10px 0 0;">'
            'Risk level based on the probability of non‑compliance.</p>',
            unsafe_allow_html=True
        )

with k3:
    with st.container(border=True):
        st.markdown('<span class="card-frame"></span>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:12.5px;font-weight:600;color:var(--ink-soft);text-transform:uppercase;'
            'letter-spacing:.05em;margin:0 0 10px;">Supplier Risk Score</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<p style="font-family:\'Fraunces\',serif;font-size:32px;font-weight:500;margin:0 0 6px;'
            f'color:var(--{badge_class});">{risk_score * 100:.1f}%</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="font-size:12.5px;color:var(--ink-faint);margin:0;">'
            'Estimated probability of non‑compliance.</p>',
            unsafe_allow_html=True
        )

st.divider()

# ------------------------------------------------------------
# AI compliance interpretation
# ------------------------------------------------------------
st.header("AI Compliance Interpretation")

if risk_score >= 0.66:
    st.markdown(f"""
    <div style="border:1px solid var(--border);border-left:4px solid var(--high);
                background:var(--paper);border-radius:16px;padding:20px 24px;">
        <p style="margin:0;">This supplier is classified as <strong style="color:var(--high);">high risk</strong>.
        The probability of non‑compliance is significant and requires close monitoring.</p>
    </div>
    """, unsafe_allow_html=True)
elif risk_score >= 0.33:
    st.markdown(f"""
    <div style="border:1px solid var(--border);border-left:4px solid var(--med);
                background:var(--paper);border-radius:16px;padding:20px 24px;">
        <p style="margin:0;">This supplier presents a <strong style="color:var(--med);">medium risk</strong>.
        Operational performance should be reviewed and monitored.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="border:1px solid var(--border);border-left:4px solid var(--low);
                background:var(--paper);border-radius:16px;padding:20px 24px;">
        <p style="margin:0;">This supplier is classified as <strong style="color:var(--low);">low risk</strong>.
        The probability of non‑compliance remains limited.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ------------------------------------------------------------
# Explainable AI (SHAP)
# ------------------------------------------------------------
shap_values = explain_prediction(pipeline, supplier_profile)

drivers = {}

for feature, value in shap_values.items():
    if "Delivery_Lead_Time" in feature:
        drivers["Delivery lead time"] = value
    if "Defect_Rate" in feature:
        drivers["Defect rate"] = value
    if "Saving_Rate" in feature:
        drivers["Saving rate"] = value

st.header("Explainable AI (SHAP)")

if drivers:
    st.markdown(
        '<p style="font-size:13.5px;color:var(--ink-soft);margin-bottom:14px;">'
        'Key operational drivers influencing this prediction:</p>',
        unsafe_allow_html=True
    )

    max_abs = max(abs(v) for v in drivers.values()) or 1

    # Each row built as a single-line string and joined below (avoids
    # Streamlit mis-rendering indented multi-line HTML as a code block)
    rows_html = []
    for i, (name, value) in enumerate(drivers.items()):
        direction = "up" if value > 0 else "down"
        tone = "high" if direction == "up" else "low"
        note = "Increases operational risk" if value > 0 else "Contributes positively to performance"
        bar_width = max(15, min(100, abs(value) / max_abs * 100))
        border_top = "border-top:1px solid var(--border);" if i > 0 else ""
        arrow_path = (
            "M12 19V5M12 5L6 11M12 5L18 11" if direction == "up"
            else "M12 5V19M12 19L6 13M12 19L18 13"
        )
        row = (
            f'<div style="display:flex;align-items:center;gap:16px;padding:14px 4px;{border_top}">'
            f'<div style="width:32px;height:32px;border-radius:9px;flex-shrink:0;'
            f'display:flex;align-items:center;justify-content:center;'
            f'background:var(--{tone}-tint);color:var(--{tone});">'
            f'<svg width="15" height="15" viewBox="0 0 24 24" fill="none">'
            f'<path d="{arrow_path}" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
            f'<div style="width:170px;font-size:14.5px;font-weight:600;flex-shrink:0;">{name}</div>'
            f'<div style="font-size:13.5px;color:var(--ink-soft);flex:1;">{note}</div>'
            f'<div style="width:160px;height:6px;background:#EFEBDF;border-radius:999px;overflow:hidden;">'
            f'<div style="height:100%;width:{bar_width:.0f}%;border-radius:999px;'
            f'background:var(--{tone});"></div></div></div>'
        )
        rows_html.append(row)

    card_html = (
        '<div style="border:1px solid var(--border);background:var(--paper);'
        'border-radius:16px;padding:6px 18px;">' + "".join(rows_html) + "</div>"
    )
    st.markdown(card_html, unsafe_allow_html=True)
else:
    st.warning(
        "No SHAP values found for the main business features. "
        "Please ensure these features exist in the model input."
    )

st.divider()

# ------------------------------------------------------------
# Business recommendations
# ------------------------------------------------------------
recommendations = []

if risk_score >= 0.66:
    recommendations.append("Reinforce monitoring and controls for upcoming orders.")
    recommendations.append("Consider alternative suppliers for critical items.")
elif risk_score >= 0.33:
    recommendations.append("Review delivery and quality performance with the supplier.")
    recommendations.append("Define improvement actions to stabilize operations.")
else:
    recommendations.append("Maintain standard monitoring procedures.")

for name, value in drivers.items():
    if name == "Delivery lead time" and value > 0:
        recommendations.append("Negotiate shorter or more reliable delivery lead times.")
    if name == "Defect rate" and value > 0:
        recommendations.append("Strengthen incoming quality inspections and KPIs.")
    if name == "Saving rate" and value < 0:
        recommendations.append("Leverage favorable commercial conditions while monitoring operations.")

st.header("Business Recommendations")

if recommendations:
    for rec in recommendations:
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:12px;padding:14px 18px;background:var(--paper);
                    border:1px solid var(--border);border-radius:12px;font-size:14.5px;margin-bottom:10px;">
            <div style="width:20px;height:20px;border-radius:6px;background:var(--pine-tint);color:var(--pine-deep);
                        display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                    <path d="M5 12L10 17L19 8" stroke="currentColor" stroke-width="2.4"
                          stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>{rec}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("No specific recommendations available for this supplier.")
