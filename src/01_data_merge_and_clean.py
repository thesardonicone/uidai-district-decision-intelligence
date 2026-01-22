import pandas as pd
import glob

# -------------------------------
# Load UIDAI datasets
# -------------------------------
enrolment = pd.concat(
    [pd.read_csv(f) for f in glob.glob("data/api_data_aadhar_enrolment_*.csv")],
    ignore_index=True
)

demographic = pd.concat(
    [pd.read_csv(f) for f in glob.glob("data/api_data_aadhar_demographic_*.csv")],
    ignore_index=True
)

biometric = pd.concat(
    [pd.read_csv(f) for f in glob.glob("data/api_data_aadhar_biometric_*.csv")],
    ignore_index=True
)

# -------------------------------
# Standardise column names
# -------------------------------
for df in [enrolment, demographic, biometric]:
    df.columns = df.columns.str.lower().str.replace(" ", "_")

# -------------------------------
# Build totals
# -------------------------------
enrolment["total_enrolment"] = (
    enrolment["age_0_5"] +
    enrolment["age_5_17"] +
    enrolment["age_18_greater"]
)

demographic["demographic_updates"] = (
    demographic["demo_age_5_17"] +
    demographic["demo_age_17_"]
)

biometric["biometric_updates"] = (
    biometric["bio_age_5_17"] +
    biometric["bio_age_17_"]
)

# -------------------------------
# Reduce columns
# -------------------------------
enrolment = enrolment[["state", "district", "total_enrolment"]]
demographic = demographic[["state", "district", "demographic_updates"]]
biometric = biometric[["state", "district", "biometric_updates"]]

# -------------------------------
# Standardise names
# -------------------------------
for df in [enrolment, demographic, biometric]:
    df["state"] = df["state"].str.upper().str.strip()
    df["district"] = df["district"].str.title().str.strip()

# -------------------------------
# Aggregate district totals
# -------------------------------
enrol_d = enrolment.groupby(["state", "district"]).sum().reset_index()
demo_d = demographic.groupby(["state", "district"]).sum().reset_index()
bio_d = biometric.groupby(["state", "district"]).sum().reset_index()

df = enrol_d.merge(demo_d, on=["state", "district"])
df = df.merge(bio_d, on=["state", "district"])

# -------------------------------
# Save intermediate
# -------------------------------
df.to_csv("output/merged_district_base.csv", index=False)

print("STEP 1 COMPLETED: Clean district-level base created")
