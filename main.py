import pandas as pd
import re
from urllib.parse import urlparse

# Load the raw company data
df = pd.read_csv('companies.csv')

# Display basic information
print("Dataset loaded successfully!")
print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print(f"\nColumn names:")
print(df.columns.to_list())

print(f"\nFirst 5 records:")
print(df.head())

print(f"\nDataset information:")
print(df.info())

print(f"\nMissing values per column:")
print(df.isnull().sum())


#Generate a data quality summary
def generate_quality_summary(df):
    summary = pd.DataFrame({
        "column_name" : df.columns,
        "missing_count" : df.isnull().sum().values,
        "missing_percentage" : (df.isnull().mean().values * 100).round(2),
        "unique_values" : df.nunique().values
    })

    return summary.sort_values(by="missing_count" , ascending=False)

quality_summary = generate_quality_summary(df)

print("\nData Quality Summary:")
print(quality_summary.to_string(index=False))


# Email validation
def is_valid_email(email):
    if pd.isna(email) or not str(email).strip():
        return False

    pattern = r"^[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, str(email).strip()))


# Phone validation : 7 to 15 digits, allowing formatting symbols
def is_valid_phone(phone):
    if pd.isna(phone):
        return False

    digits = re.sub(r"\D","",str(phone))
    return 7 <= len(digits) <= 15


# Website validation
def is_valid_website(website):
    if pd.isna(website) or not str(website).strip():
        return False

    url = str(website).strip()
    parsed = urlparse(url)

    return (
        parsed.scheme in ("http","https")
        and bool(parsed.netloc)
        and "." in parsed.netloc
    )


# Date validtaion
def is_valid_date(date_value):
    if pd.isna(date_value) or not str(date_value).strip():
        return False

    try:
        pd.to_datetime(date_value, format= "%Y-%m-%d", errors= "raise")
        return True
    except(ValueError, TypeError):
        return False


# Apply validation rules
df["invalid_email"] = ~df["email"].apply(is_valid_email)
df["invalid_phone"] = ~df["phone"].apply(is_valid_phone)
df["invalid_website"] = ~df["company_website"].apply(is_valid_website)
df["invalid_date"] = ~df["last_verified_date"].apply(is_valid_date)


# Display invalid record counts
print("\nValidation Resuls:")
print(f"Invalid emails: {df['invalid_email'].sum()}")
print(f"Invalid phones: {df['invalid_phone'].sum()}")
print(f"Invalid websites: {df['invalid_website'].sum()}")
print(f"Invalid dates: {df['invalid_date'].sum()}")


# Create a report of records that failed validation
validation_columns = [
    "invalid_email",
    "invalid_phone",
    "invalid_website",
    "invalid_date"
]
invalid_records = df[df[validation_columns].any(axis=1)].copy()

print("\nInvalid Record Report:")
print(f"Total record require review: {len(invalid_records)}")

print(invalid_records[
    ["record_id", "company_name", "email", "phone"]
    + validation_columns
].head(10).to_string(index=False)
)


invalid_records.to_csv("invalid_records_report.csv", index=False)
print("\nInvalid records report saved successfully!")


def get_validate_errors(row):
    errors = []

    if row["invalid_email"]:
        errors.append("Invalid or missing email")

    if row["invalid_phone"]:
        errors.append("Invalid phone format")

    if row["invalid_website"]:
        errors.append("Invalid website URL")

    if row["invalid_date"]:
        errors.append("Invalid date format")

    return ", ".join(errors)


# Add a readable explanation for each flagged record
invalid_records["validation_errors"] = invalid_records.apply(get_validate_errors, axis=1)

# Export the improved report
invalid_records.to_csv("invalid_records_report.csv", index=False)
print("\nUpdated records with validation errors saved!")
print(invalid_records[["record_id", "company_name", "validation_errors"]].head(10).to_string(index=False))


# Detect exact duplicates in original dataset
exact_duplicates = df.duplicated(keep=False)

duplicate_records = df[exact_duplicates].copy()

print("\nDuplicate deletion results:")
print(f"Total rows involved in exact duplicates: {len(duplicate_records)}")
print(duplicate_records[["record_id", "company_name", "email"]].head(10).to_string(index=False))

# Export exact duplicate records for review
duplicate_records.to_csv("exact_duplicates_report.csv", index=False)
print("\nExact duplicate report were saved successfully!")


# Normalize emails to help identify near-duplicates
df["normalized_email"] = df["email"].fillna("").str.strip().str.lower()

# Find repeated, non-empty email addresses
valid_email_values = df["normalized_email"].ne("") 

near_duplicate_mask = (df["normalized_email"].duplicated(keep=False) & valid_email_values)

near_duplicate_records = df[near_duplicate_mask].copy()

print("\nNear-Duplicate email results:")
print(f"Rows involved in repeated email addresses: {len(near_duplicate_records)}")

print(near_duplicate_records[
    ["record_id", "company_name", "email", "normalized_email"]
    ].head(10).to_string(index=False))


# Export near-duplicate email records for review
near_duplicate_records.to_csv("near_duplicate_emails_report.csv", index=False)
print("\nNear-duplicate email report saved successfully!")


# Final data quality summary
total_records = len(df)

summary = {
    "metric" : [
        "Total records processed",
        "Records with missing values",
        "Invalid emails",
        "Invalid phones",
        "Invalid websites",
        "Invalid dates",
        "Rows involved in exact duplicates",
        "Rows involved in repeated email addresses",
        "Records requiring review"
    ],
    "count" : [
        len(df),
        df.isnull().any(axis=1).sum(),
        df["invalid_email"].sum(),
        df["invalid_phone"].sum(),
        df["invalid_website"].sum(),
        df["invalid_date"].sum(),
        len(duplicate_records),
        len(near_duplicate_records),
        len(invalid_records)
    ]
}

summary_df = pd.DataFrame(summary)

# print(summary_df.dtypes)
# print(summary_df["count"].tolist())

# summary_df["count"] = pd.to_numeric(summary_df["count"], errors="raise")

summary_df["percentage"] = (
    summary_df["count"] / total_records * 100
).round(2)

summary_df.to_csv("data_quality_summary.csv" , index=False)

print("\nFinal Data Quality Summary:")
print(summary_df.to_string(index=False))

print("\nData quality symmary saved successfully!")