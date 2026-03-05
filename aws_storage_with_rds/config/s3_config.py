import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION")   # Change to your region
S3_BUCKET_NAME =  os.getenv("S3_BUCKET_NAME")# Must be globally unique

# Local file paths
LOCAL_RAW_FILE =  os.getenv("LOCAL_RAW_FILE")  # Path to your local CSV
LOCAL_DOWNLOAD_PATH = os.getenv("LOCAL_DOWNLOAD_PATH") 
LOCAL_PROCESS_DOWNLOAD_PATH = os.getenv("LOCAL_PROCESS_DOWNLOAD_PATH") 

# S3 folder structure
S3_RAW_PREFIX = "raw/"
S3_PROCESSED_PREFIX = "processed/"

RAW_PATH = os.getenv("RAW_PATH")
PROCESSED_PATH = os.getenv("PROCESSED_PATH")
MONTHLY_SUMMARY_PATH = os.getenv("MONTHLY_SUMMARY_PATH")


def get_s3_client():
    """
    Initialize and return an S3 client.
    Keeping this inside config ensures all scripts use the same region and setup.
    """
    return boto3.client("s3", region_name=AWS_REGION)


