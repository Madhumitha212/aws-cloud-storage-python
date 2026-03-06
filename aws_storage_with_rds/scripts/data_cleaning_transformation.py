import pandas as pd
import io
from botocore.exceptions import ClientError
from config.s3_config import S3_BUCKET_NAME, get_s3_client

def read_from_s3(file_key):
    try:
        s3 = get_s3_client()

        response = s3.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_key
        )

        df = pd.read_csv(io.BytesIO(response["Body"].read()))

        print("File successfully read from S3")
        return df

    except ClientError as e:
        print(f"Error reading from S3: {e}")
        raise


def clean_data(df):
    print("Cleaning data...")

    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    df["price_per_unit"] = df["price_per_unit"].fillna(
        df["price_per_unit"].median()
    )

    df["quantity"] = df["quantity"].astype(int)
    df["discount_percent"] = df["discount_percent"].astype(float)

    print("Data cleaning completed")

    return df


def generate_aggregations(df):

    print("Generating aggregations...")

    total_revenue = df["final_amount"].sum()
    average_order_value = df["final_amount"].mean()
    total_transactions = df["transaction_id"].count()

    print(f"Total Revenue: {total_revenue}")
    print(f"Average Order Value: {average_order_value}")
    print(f"Total Transactions: {total_transactions}")

    df["month"] = df["transaction_date"].dt.to_period("M")

    monthly_summary = (
        df.groupby("month")["final_amount"]
        .sum()
        .reset_index()
    )

    return df, monthly_summary


def upload_to_s3(df, file_key):

    try:
        s3 = get_s3_client()

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_key,
            Body=csv_buffer.getvalue()
        )

        print(f"Uploaded successfully to {file_key}")

    except ClientError as e:
        print(f"Upload failed: {e}")
        raise

def main():

    df = read_from_s3("raw/sales_transactions.csv")
    df = clean_data(df)
    cleaned_df, monthly_summary = generate_aggregations(df)
    upload_to_s3(cleaned_df, "processed/cleaned_sales.csv")
    upload_to_s3(monthly_summary, "processed/monthly_summary.csv")

    print("Data pipeline completed successfully")


if __name__ == "__main__":
    main()