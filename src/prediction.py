from pathlib import Path
import joblib
import pandas as pd
import numpy as np
import shap

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_pipeline():
    model_path = PROJECT_ROOT / "models" / "procuresense_pipeline.pkl"
    return joblib.load(model_path)


def load_data():
    data_path = PROJECT_ROOT / "data" / "prediction" / "procurement_features.csv"
    return pd.read_csv(data_path)


def predict_supplier(pipeline, supplier_row: pd.Series):
    X = supplier_row.to_frame().T
    proba = pipeline.predict_proba(X)[0]
    p_no = float(proba[0])

    if p_no >= 0.66:
        risk_label = "High risk"
    elif p_no >= 0.33:
        risk_label = "Medium risk"
    else:
        risk_label = "Low risk"

    return risk_label, p_no


def explain_prediction(pipeline, supplier_row: pd.Series):
    model = pipeline.named_steps["classifier"]
    preprocessed = pipeline.named_steps["preprocessor"].transform(
        supplier_row.to_frame().T
    )

    background = np.zeros(preprocessed.shape)

    def predict_fn(x):
        return model.predict_proba(x)[:, 0]

    explainer = shap.KernelExplainer(predict_fn, background)
    shap_values = explainer.shap_values(preprocessed)

    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    return dict(zip(feature_names, shap_values[0]))
