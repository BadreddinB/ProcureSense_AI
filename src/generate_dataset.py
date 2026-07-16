import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random

# ---------------------------------------
# Configuration
# ---------------------------------------
N = 10000  # number of rows

# ---------------------------------------
# Supplier list (50 unique suppliers)
# ---------------------------------------
suppliers = [
    "Alpha Inc", "Beta Supplies", "Gamma Co", "Delta Logistics", "Epsilon Group",
    "FerroTech", "RailSystems", "ElectroParts", "MechaWorks", "NovaRail",
    "EuroParts", "IndusPrime", "MetalWorks", "OptiRail", "RailCom",
    "TechMotion", "CoreParts", "PrimeRail", "RailDynamics", "MegaParts",
    "SteelLine", "RailPro", "MotionTech", "IndusRail", "RailEdge",
    "ProParts", "RailMaster", "ElectroRail", "MechaPrime", "RailFusion",
    "RailNova", "IndusCore", "RailSphere", "RailPulse", "RailLink",
    "RailForge", "RailWorks", "RailCraft", "RailEngine", "RailParts",
    "RailSupply", "RailSystems+", "RailMotion", "RailTech", "RailVector",
    "Alstraileco", "RailDynamics+", "RailCore+", "RailOptima", "RailAdvance"
]

# ---------------------------------------
# Industrial item categories
# ---------------------------------------
item_categories = [
    "Control Electronics",
    "Cabling & Harnesses",
    "Traction Motors",
    "Brake Systems",
    "HVAC Systems",
    "Doors & Access Systems",
    "Interior Components",
    "Body Structures",
    "Bogies & Wheelsets",
    "Maintenance & MRO"
]

order_statuses = [
    "Delivered", "Pending", "Partially Delivered", "Cancelled"
]

# ---------------------------------------
# Generate dataset
# ---------------------------------------
np.random.seed(42)

data = {
    "PO_ID": np.arange(1, N + 1),
    "Supplier": np.random.choice(suppliers, N),
    "Item_Category": np.random.choice(item_categories, N),
    "Order_Status": np.random.choice(order_statuses, N, p=[0.72, 0.15, 0.10, 0.03]),
}

# Generate realistic dates
start_date = datetime(2023, 1, 1)
order_dates = [start_date + timedelta(days=int(np.random.uniform(0, 365))) for _ in range(N)]

delivery_dates = [
    order_dates[i] + timedelta(days=int(np.random.uniform(2, 150)))
    for i in range(N)
]

data["Order_Date"] = order_dates
data["Delivery_Date"] = delivery_dates

# Quantities
data["Quantity"] = np.random.randint(1, 500, N)

# Unit prices
data["Unit_Price"] = np.round(np.random.uniform(5, 500, N), 2)

# Negotiated prices (1–40% discount)
negotiated_prices = []
for up in data["Unit_Price"]:
    discount = np.random.uniform(0.05, 0.40)
    negotiated_prices.append(round(up * (1 - discount), 2))

data["Negotiated_Price"] = negotiated_prices

# Defective units (0–20% of quantity)
data["Defective_Units"] = [
    int(q * np.random.uniform(0, 0.20)) for q in data["Quantity"]
]

# ---------------------------------------
# Compliance calculation (calibrated for ~20% non-compliant)
# ---------------------------------------
compliance = []
for i in range(N):
    delay = (data["Delivery_Date"][i] - data["Order_Date"][i]).days
    defects = data["Defective_Units"][i]
    discount = data["Unit_Price"][i] - data["Negotiated_Price"][i]

    risk_score = (
        (delay / 150) * 0.5 +                          # delays matter a lot
        (defects / max(data["Quantity"][i], 1)) * 0.4 + # defects matter heavily
        (discount / data["Unit_Price"][i]) * 0.1        # discount matters less
    )

    compliance.append(1 if risk_score < 0.45 else 0)

data["Compliance"] = compliance

# ---------------------------------------
# Export CSV 
# ---------------------------------------
df = pd.DataFrame(data)

output_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "procurement_data.csv"
df.to_csv(output_path, index=False)

print(df.head())
print(f"\nDataset saved to: {output_path}")
