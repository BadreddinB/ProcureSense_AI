from pathlib import Path
import sys

import streamlit as st
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.prediction import load_pipeline, load_data, predict_supplier, explain_prediction

st.set_page_config(
    page_title="ProcureSense AI",
    page_icon="📊",
    layout="wide"
)

pipeline = load_pipeline()
data = load_data()

st.title("📊 ProcureSense AI")
st.subheader("Supplier Risk & Performance Intelligence")
st.divider()

st.header("Project Overview")
st.write("""
ProcureSense AI transforms procurement data into actionable insights,
helping teams evaluate supplier risk, monitor performance,
and strengthen operational reliability.
""")
st.divider()

st.header("Supplier Risk Prediction")

selected_supplier = st.selectbox(
    "Select a supplier",
    options=sorted(data["Supplier"].unique())
)

supplier_profile = data[data["Supplier"] == selected_supplier].iloc[0]
st.divider()

st.header("Supplier Profile")

total_cost_saving = round(
    supplier_profile["Cost_Saving"] * supplier_profile["Quantity"],
    2
)

profile_df = pd.DataFrame(
    {
        "Attribute": [
            "Supplier",
            "Item Category",
            "Quantity",
            "Estimated Spend (value)",
            "Total Cost Saving (value)",
        ],
        "Value": [
            selected_supplier,
            supplier_profile["Item_Category"],
            f"{int(supplier_profile['Quantity']):,} units",
            f"{supplier_profile['Estimated_Spend']:,.2f}",
            f"{total_cost_saving:,.2f}",
        ],
    }
)

st.table(profile_df)
st.divider()

st.header("Procurement KPIs")

kpi_col1, kpi_col2 = st.columns(2)

with kpi_col1:
    compliance_rate = data["Compliance"].mean()
    st.metric(
        "Overall Supplier Compliance Rate",
        f"{compliance_rate * 100:.1f} %",
        help="Percentage of purchase orders classified as compliant."
    )

risk_label, risk_score = predict_supplier(pipeline, supplier_profile)

def risk_color(score: float) -> str:
    if score < 0.33:
        return "🟢 Low"
    elif score < 0.66:
        return "🟠 Medium"
    else:
        return "🔴 High"

with kpi_col2:
    st.metric(
        "Supplier Risk",
        risk_color(risk_score),
        help="Risk level based on the probability of non‑compliance."
    )
    st.metric(
        "Supplier Risk Score",
        f"{risk_score * 100:.1f} %",
        help="Estimated probability of non‑compliance."
    )

st.divider()

st.header("AI Compliance Interpretation")

if risk_score >= 0.66:
    st.write("""
This supplier is classified as **high risk**.
The probability of non‑compliance is significant and requires close monitoring.
""")
elif risk_score >= 0.33:
    st.write("""
This supplier presents a **medium risk**.
Operational performance should be reviewed and monitored.
""")
else:
    st.write("""
This supplier is classified as **low risk**.
The probability of non‑compliance remains limited.
""")

st.divider()

st.header("Explainable AI (SHAP)")

shap_values = explain_prediction(pipeline, supplier_profile)

drivers = {}

for feature, value in shap_values.items():
    if "Delivery_Lead_Time" in feature:
        drivers["Delivery lead time"] = value
    if "Defect_Rate" in feature:
        drivers["Defect rate"] = value
    if "Saving_Rate" in feature:
        drivers["Saving rate"] = value

if drivers:
    st.write("Key operational drivers influencing this prediction:")
    for name, value in drivers.items():
        if value > 0:
            st.markdown(f"- **{name}** increases operational risk.")
        else:
            st.markdown(f"- **{name}** contributes positively to performance.")
else:
    st.warning(
        "No SHAP values found for the main business features. "
        "Please ensure these features exist in the model input."
    )

st.divider()

st.header("Business Recommendations")

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

if recommendations:
    st.write("Recommended actions:")
    for rec in recommendations:
        st.markdown(f"- {rec}")
else:
    st.write("No specific recommendations available for this supplier.")
