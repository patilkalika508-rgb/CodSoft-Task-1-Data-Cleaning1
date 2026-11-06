import pandas as pd
from pathlib import Path

# --------------------------------------------------
# TASK 1 : DATA CLEANING & PREPROCESSING
# --------------------------------------------------

# Load the dataset
file_path = "sales_data.csv"

raw = pd.read_csv(file_path)

print("\nFIRST FIVE ROWS")
print(raw.head())

print("\nNUMBER OF ROWS AND COLUMNS")
print(raw.shape)

print("\nCOLUMN TYPES AND NON-MISSING COUNTS")
print(raw.info())

# --------------------------------------------------
# CHECK MISSING VALUES
# --------------------------------------------------

print("\nMISSING VALUES IN EACH COLUMN")
print(raw.isna().sum())

# --------------------------------------------------
# CHECK EXACT DUPLICATE ROWS
# --------------------------------------------------

print("\nEXACT DUPLICATE ROWS")
print(raw.duplicated().sum())

# --------------------------------------------------
# CHECK CITY VALUES
# --------------------------------------------------

if "City" in raw.columns:
    print("\nCITY VALUES BEFORE CLEANING")
    print(raw["City"].value_counts(dropna=False))

# Keep the original data unchanged
# and clean a copy

data = raw.copy()

# --------------------------------------------------
# CLEAN TEXT COLUMNS
# --------------------------------------------------

text_columns = ["City", "Product", "Category", "PaymentMethod"]

for column in text_columns:

    if column in data.columns:

        data[column] = (
            data[column]
            .astype("string")
            .str.strip()
            .str.title()
        )

# --------------------------------------------------
# CONVERT NUMERIC COLUMNS
# --------------------------------------------------

numeric_columns = ["Age", "Quantity", "UnitPrice"]

for column in numeric_columns:

    if column in data.columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

# --------------------------------------------------
# CONVERT ORDER DATE
# --------------------------------------------------

if "OrderDate" in data.columns:

    data["OrderDate"] = pd.to_datetime(
        data["OrderDate"],
        format="mixed",
        errors="coerce"
    )

# --------------------------------------------------
# REMOVE DUPLICATE ORDER IDs
# --------------------------------------------------

if "OrderID" in data.columns:

    data = data.drop_duplicates(
        subset=["OrderID"],
        keep="first"
    )

# --------------------------------------------------
# HANDLE MISSING VALUES
# --------------------------------------------------

if "Age" in data.columns:
    data["Age"] = data["Age"].fillna(
        data["Age"].median()
    )

if "Quantity" in data.columns:
    data["Quantity"] = data["Quantity"].fillna(0)

if "UnitPrice" in data.columns:
    data["UnitPrice"] = data["UnitPrice"].fillna(
        data["UnitPrice"].median()
    )

# Fill missing text values

for column in ["City", "Product", "Category", "PaymentMethod"]:

    if column in data.columns:

        data[column] = data[column].fillna("Unknown")

# --------------------------------------------------
# CREATE USEFUL COLUMNS FOR ANALYSIS
# --------------------------------------------------

if "Quantity" in data.columns and "UnitPrice" in data.columns:

    data["Sales"] = (
        data["Quantity"] * data["UnitPrice"]
    )

if "OrderDate" in data.columns:

    data["Month"] = (
        data["OrderDate"]
        .dt.to_period("M")
        .astype(str)
    )

# --------------------------------------------------
# SAVE CLEANED DATASET
# --------------------------------------------------

output_folder = Path("cleaned_data")
output_folder.mkdir(exist_ok=True)

cleaned_file = output_folder / "sales_cleaned.csv"

data.to_csv(
    cleaned_file,
    index=False
)

print("\nCLEANED DATA SAVED SUCCESSFULLY")
print(cleaned_file)

# --------------------------------------------------
# CHECK DATA AFTER CLEANING
# --------------------------------------------------

print("\nMISSING VALUES AFTER CLEANING")
print(data.isna().sum())

print("\nCLEANED DATA TYPES")
print(data.dtypes)

print("\nFIRST FIVE ROWS AFTER CLEANING")
print(data.head())