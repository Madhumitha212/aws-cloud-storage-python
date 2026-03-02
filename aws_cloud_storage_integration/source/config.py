import os

# AWS configuration
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
BUCKET_NAME = os.getenv("BUCKET_NAME", "aws-storage-project-bucket")

# Small file
LOCAL_SMALL_FILE = os.getenv("LOCAL_SMALL_FILE", "/mnt/d/aws_cloud_storage/aws_cloud_storage_integration/datasets/small_file.csv")
S3_SMALL_KEY = os.getenv("S3_SMALL_KEY", "small_file.csv")

# Large file
LOCAL_LARGE_FILE = os.getenv("LOCAL_LARGE_FILE", "/mnt/d/aws_cloud_storage/aws_cloud_storage_integration/datasets/large_file.log")
S3_LARGE_KEY = os.getenv("S3_LARGE_KEY", "large_file.log")

# Download paths
LOCAL_DOWNLOAD_SMALL = os.getenv("LOCAL_DOWNLOAD_SMALL", "/mnt/d/aws_cloud_storage/aws_cloud_storage_integration/downloads/small_file.csv")
LOCAL_DOWNLOAD_LARGE = os.getenv("LOCAL_DOWNLOAD_LARGE", "/mnt/d/aws_cloud_storage/aws_cloud_storage_integration/downloads/large_file.log")