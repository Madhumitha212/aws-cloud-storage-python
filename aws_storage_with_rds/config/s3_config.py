import boto3

# AWS Configuration
AWS_REGION = "ap-south-1"   # Change to your region
S3_BUCKET_NAME = "aws-storage-rds-bucket"  # Must be globally unique

# Local file paths
LOCAL_RAW_FILE = "/mnt/d/aws_cloud_storage/aws_storage_with_rds/dataset/sales_transactions.csv"   # Path to your local CSV
LOCAL_DOWNLOAD_PATH = "/mnt/d/aws_cloud_storage/aws_storage_with_rds/downloads/sales_transactions.csv"
LOCAL_PROCESS_DOWNLOAD_PATH = "/mnt/d/aws_cloud_storage/aws_storage_with_rds/downloads/cleaned_sales.csv"

# S3 folder structure
S3_RAW_PREFIX = "raw/"
S3_PROCESSED_PREFIX = "processed/"

RAW_PATH = f"s3://{S3_BUCKET_NAME}/raw/sales_transactions.csv"
PROCESSED_PATH = f"s3://{S3_BUCKET_NAME}/processed/cleaned_sales.csv"
MONTHLY_SUMMARY_PATH = f"s3://{S3_BUCKET_NAME}/processed/monthly_summary.csv"


def get_s3_client():
    """
    Initialize and return an S3 client.
    Keeping this inside config ensures all scripts use the same region and setup.
    """
    return boto3.client("s3", region_name=AWS_REGION)


