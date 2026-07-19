# ProcureSense AI

### AI-Powered Supplier Risk Assessment for Procurement Decision Support

🔗 **Live Demo:** https://procuresense-ai.streamlit.app/

ProcureSense AI is an end-to-end Machine Learning application that helps procurement teams assess supplier compliance risk before purchase orders are executed.

The project combines predictive analytics with Explainable AI (SHAP) to transform procurement data into transparent, business-oriented insights. It demonstrates how AI can support procurement professionals by predicting supplier compliance risk and explaining every prediction in language that facilitates business decision-making.

---

# Business Context

Supplier performance has a direct impact on procurement efficiency, operational costs and supply chain reliability. Delays, quality issues and poor contract execution can lead to production disruptions, increased purchasing costs and lower customer satisfaction.

Although procurement teams routinely monitor supplier KPIs, these indicators are often reviewed after operational issues have already occurred.

ProcureSense AI explores how Machine Learning can support procurement by estimating supplier compliance risk before purchase orders are approved, enabling more proactive supplier management.

---

# Business Problem

This project investigates the following questions:

- Can supplier compliance be predicted from procurement data?
- Which operational factors contribute most to supplier compliance?
- Can Explainable AI improve trust in machine learning predictions?
- Can predictive analytics be translated into practical procurement recommendations?

---

# Project Objectives

The project aims to:

- Develop a realistic synthetic procurement dataset representing railway procurement operations.
- Explore procurement activities, supplier performance and purchasing behaviour.
- Engineer business-oriented features from procurement data.
- Train and compare multiple classification models.
- Select the strongest-performing model using cross-validation.
- Explain individual predictions using SHAP.
- Deliver an interactive Streamlit application for procurement professionals.

---

# Dataset

| | |
|---|---|
| **Source** | Synthetic dataset |
| **Industry** | Railway procurement |
| **Purchase Orders** | 10,000 |
| **Suppliers** | 50 |
| **Item Categories** | 10 |
| **Period** | 2023–2024 |
| **Missing Values** | None |
| **Target Variable** | Supplier Compliance |

Public procurement datasets rarely contain the level of operational detail required for supplier risk modelling. To address this limitation, a synthetic dataset was generated using a reproducible Python pipeline that simulates realistic procurement operations, including supplier performance, pricing, delivery behaviour and product quality.

---

# Methodology

The project follows a structured end-to-end Machine Learning workflow organised across three notebooks.

### Notebook 01 — Data Loading

- Load the synthetic procurement dataset.
- Validate structure, data types and completeness.

### Notebook 02 — Exploratory Data Analysis

- Explore procurement activities.
- Analyse supplier performance.
- Study purchasing behaviour.
- Identify relationships between operational KPIs.

### Notebook 03 — Predictive Modeling

- Engineer business-oriented features.
- Prepare the modelling dataset.
- Train multiple classification models.
- Evaluate predictive performance.
- Select the final model.
- Export the deployment pipeline.

---

# Feature Engineering

Several procurement-oriented features were engineered to improve predictive performance.

| Feature | Business Purpose |
|---|---|
| Delivery Lead Time | Measure supplier responsiveness |
| Cost Saving | Quantify negotiated savings |
| Saving Rate | Standardise procurement savings |
| Defect Rate | Measure delivered product quality |

These engineered variables provide additional business context beyond the original procurement data.

---

# Predictive Modeling

Three supervised classification algorithms were evaluated using the same preprocessing pipeline to ensure a fair comparison.

- Logistic Regression
- Random Forest
- XGBoost

Model evaluation combines multiple complementary metrics, including:

- Accuracy
- Classification Report
- Confusion Matrix
- 5-Fold Cross-Validation

The final deployment pipeline is selected automatically according to the highest cross-validation Macro F1-score.

---

# Explainable AI

ProcureSense AI integrates SHAP to explain every prediction.

Instead of presenting mathematical feature contributions, SHAP outputs are translated into procurement-oriented language.

For example:

> Longer delivery lead times increase supplier risk.

rather than

> Delivery_Lead_Time has a positive SHAP value.

This improves model transparency and helps business users understand why a supplier has been classified as compliant or non-compliant.

---

# Dashboard

The Streamlit application is designed for procurement professionals.

It provides:

- Supplier profile overview
- Compliance risk prediction
- SHAP-based explanations
- Business-oriented procurement recommendations

The dashboard focuses on supporting procurement decision-making rather than exposing technical machine learning metrics.

---

# Business Value

ProcureSense AI demonstrates how Machine Learning and Explainable AI can support procurement processes without replacing human expertise.

The application helps procurement teams:

- anticipate supplier compliance risks;
- understand the operational drivers behind predictions;
- prioritise supplier monitoring;
- support sourcing decisions with transparent, data-driven insights.

---

# Project Structure

```text
ProcureSense_AI/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── prediction/
│
├── models/
│   └── procuresense_pipeline.pkl
│
├── notebooks/
│   ├── 01_data_loading.ipynb
│   ├── 02_eda.ipynb
│   └── 03_predictive_modeling.ipynb
│
├── src/
│   ├── generate_dataset.py
│   ├── prediction.py
│   ├── shap_explainer.py
│   ├── recommendations.py
│   └── helpers.py
│
├── streamlit_app/
│   └── app.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SHAP
- Matplotlib
- Streamlit
- Joblib
- Docker

---

# Reproducibility

Clone the repository:

```bash
git clone https://github.com/BadreddinB/ProcureSense_AI.git
cd ProcureSense_AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the dataset:

```bash
python src/generate_dataset.py
```

Run the notebooks sequentially:

```text
01_data_loading.ipynb
02_eda.ipynb
03_predictive_modeling.ipynb
```

Launch the Streamlit application:

```bash
streamlit run streamlit_app/app.py
```
Or run with Docker:

```bash
docker build -t procuresense-ai .
docker run -p 8501:8501 procuresense-ai
Then open http://localhost:8501 in your browser.
```
The Dockerfile is included to provide a portable, reproducible execution environment.
---

# Limitations

This project is intended as a Machine Learning demonstration rather than a production-ready procurement platform.

Current limitations include:

- Synthetic procurement dataset
- Binary classification only
- Limited supplier history
- No ERP integration
- No real-time data ingestion
- No automated model retraining

---

# Future Improvements

Potential future enhancements include:

- Validation on real procurement data
- Multi-class supplier risk scoring
- Supplier segmentation
- Historical trend analysis
- Supplier dependency analysis
- ERP integration (SAP / Oracle)
- Automated model monitoring
- CI/CD deployment pipeline
- Cloud deployment
- User authentication

---

# License

This project was developed for educational and portfolio purposes to demonstrate an end-to-end Machine Learning workflow applied to procurement analytics.
