import pandas as pd
import numpy as np

df = pd.read_csv("output/merged_district_base.csv")

# -------------------------------
# Rate calculations
# -------------------------------
df["biometric_rate"] = df["biometric_updates"] / df["total_enrolment"]
df["demographic_rate"] = df["demographic_updates"] / df["total_enrolment"]

# -------------------------------
# Signal construction
# -------------------------------

# Migration Stress Signal
df["MSS"] = df["demographic_rate"] * 1000

# Labour Wear Signal
df["LWS"] = df["biometric_rate"] / (df["demographic_rate"] + 0.00001)

# Service Overload Signal
df["SOS"] = df["biometric_rate"]

# Irregular Risk Signal
df["IRS"] = np.where(
    (df["biometric_rate"] > df["biometric_rate"].quantile(0.75)) &
    (df["demographic_rate"] < df["demographic_rate"].median()),
    1, 0
)

# Inclusion Stress Signal
df["INS"] = np.where(
    (df["biometric_rate"] > df["biometric_rate"].quantile(0.75)) &
    (df["demographic_rate"] < df["demographic_rate"].quantile(0.25)),
    1, 0
)

# -------------------------------
# Normalise scores (0–100)
# -------------------------------
for col in ["MSS", "LWS", "SOS"]:
    df[col + "_score"] = (df[col] / df[col].max()) * 100

df["IRS_score"] = df["IRS"] * 100
df["INS_score"] = df["INS"] * 100

# -------------------------------
# Dominant signal
# -------------------------------
signal_cols = [
    "MSS_score", "LWS_score",
    "SOS_score", "IRS_score", "INS_score"
]

df["dominant_signal"] = df[signal_cols].idxmax(axis=1)

# -------------------------------
# UIDAI action mapping
# -------------------------------
def recommend_action(sig):
    if sig == "MSS_score":
        return "Deploy mobile enrolment units"
    if sig == "LWS_score":
        return "Upgrade biometric capture devices"
    if sig == "SOS_score":
        return "Increase Aadhaar operator capacity"
    if sig == "IRS_score":
        return "Conduct audit and quality checks"
    if sig == "INS_score":
        return "Run assisted biometric update camps"
    return "Monitor"

df["uidai_action"] = df["dominant_signal"].apply(recommend_action)

# -------------------------------
# Overall risk score
# -------------------------------
df["overall_risk_score"] = df[signal_cols].mean(axis=1)

# -------------------------------
# Save final intelligence file
# -------------------------------
df.to_csv("output/district_decision_intelligence.csv", index=False)

print("STEP 2 COMPLETED: District decision intelligence generated")
