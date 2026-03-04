import pandas as pd
from botocore.exceptions import NoCredentialsError, ClientError
from config.s3_config import *


def read_from_s3():
    try:
        df = pd.read_csv(RAW_PATH)
        print("File successfully read from S3")
        return df
    except NoCredentialsError:
        print(" AWS credentials not found")
        raise
    except Exception as e:
        print(f" Error reading from S3: {e}")
        raise

def clean_data(df):
    print(" Cleaning data...")

    # Convert date column
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # Handle missing values using median
    df["price_per_unit"] = df["price_per_unit"].fillna(
        df["price_per_unit"].median()
    )

    # Ensure numeric types
    df["quantity"] = df["quantity"].astype(int)
    df["discount_percent"] = df["discount_percent"].astype(float)

    print("Data cleaning completed")
    return df

def generate_aggregations(df):
    print("Generating aggregations...")

    # Summary metrics
    total_revenue = df["final_amount"].sum()
    average_order_value = df["final_amount"].mean()
    total_transactions = df["transaction_id"].count()

    print(f"Total Revenue: {total_revenue}")
    print(f"Average Order Value: {average_order_value}")
    print(f"Total Transactions: {total_transactions}")

    # Monthly aggregation
    df["month"] = df["transaction_date"].dt.to_period("M")
    monthly_summary = (
        df.groupby("month")["final_amount"]
        .sum()
        .reset_index()
    )

    return df, monthly_summary

def upload_to_s3(df, path):
    try:
        df.to_csv(path, index=False)
        print(f"Uploaded to {path}")
    except ClientError as e:
        print(f"Upload failed: {e}")
        raise

def main():
    df = read_from_s3()
    df = clean_data(df)
    cleaned_df, monthly_summary = generate_aggregations(df)

    upload_to_s3(cleaned_df, PROCESSED_PATH)
    upload_to_s3(monthly_summary, MONTHLY_SUMMARY_PATH)

    print("Data pipeline completed successfully")
   

if __name__ == "__main__":
    main()