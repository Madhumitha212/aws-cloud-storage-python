import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION")   # Change to your region
S3_BUCKET_NAME =  os.getenv("S3_BUCKET_NAME")# Must be globally unique

_s3_client = None

def get_s3_client():
    global _s3_client

    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            region_name=AWS_REGION
        )

    return _s3_client


