import pandas as pd
import os

# === FILE PATHS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
payment_file = os.path.join(BASE_DIR, "pay2.xlsx")
participants_file = os.path.join(BASE_DIR, "unverified1(rough).xlsx")

# === READ FILES ===
payment_df = pd.read_excel(payment_file, dtype=str)  # Read all as strings
participants_df = pd.read_excel(participants_file, dtype=str)

utr_col = "UTR Number / Transaction ID"
if utr_col not in participants_df.columns:
    raise ValueError(f"Column '{utr_col}' not found in participants file.")

# Convert payment sheet to one big string for searching
payment_text = " ".join(payment_df.astype(str).fillna("").stack().tolist())

def utr_found(utr):
    if pd.isna(utr) or utr.strip() == "":
        return False
    utr_str = str(utr).strip()
    return utr_str in payment_text

participants_df["Verified"] = participants_df[utr_col].apply(utr_found)

# Split into verified/unverified
verified_df = participants_df[participants_df["Verified"] == True].drop(columns=["Verified"])
unverified_df = participants_df[participants_df["Verified"] == False].drop(columns=["Verified"])

# Save results
verified_df.to_excel(os.path.join(BASE_DIR, "verified2.xlsx"), index=False)
unverified_df.to_excel(os.path.join(BASE_DIR, "unverified2.xlsx"), index=False)

print(f"✅ Verification completed.\nVerified: {len(verified_df)}\nUnverified: {len(unverified_df)}")
