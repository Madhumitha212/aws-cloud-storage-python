import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError


# ----------------------------
# Create S3 Client
# ----------------------------
def create_s3_client(region):
    return boto3.client("s3", region_name=region)


# ----------------------------
# Download File
# ----------------------------
def download_file(bucket_name, s3_key, local_path, region):
    try:
        s3 = create_s3_client(region)

        print(f"Downloading '{s3_key}' from bucket '{bucket_name}'...")
        s3.download_file(bucket_name, s3_key, local_path)
        print("Download successful")

        return True

    except NoCredentialsError:
        print("AWS credentials not found.")
        return False

    except ClientError as e:
        print("AWS Client Error:", e)
        return False

    except Exception as e:
        print("Unexpected error:", e)
        return False


# ----------------------------
# Verify Integrity by File Size
# ----------------------------
def verify_by_size(bucket_name, s3_key, local_path, region):
    try:
        s3 = create_s3_client(region)

        # Get S3 file size
        response = s3.head_object(Bucket=bucket_name, Key=s3_key)
        s3_size = response["ContentLength"]

        # Get local file size
        local_size = os.path.getsize(local_path)

        print("\nVerifying file integrity (by file size)...")
        print("S3 File Size   :", s3_size, "bytes")
        print("Local File Size:", local_size, "bytes")

        if s3_size == local_size:
            print("File integrity verified")
        else:
            print("Integrity mismatch")

    except Exception as e:
        print("Verification error:", e)


# ----------------------------
# List Files in Bucket / Prefix
# ----------------------------
def list_files(bucket_name, prefix, region):
    try:
        s3 = create_s3_client(region)

        response = s3.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )

        print(f"\nFiles in bucket '{bucket_name}' with prefix '{prefix}':\n")

        if "Contents" in response:
            for obj in response["Contents"]:
                print(obj["Key"])
        else:
            print("No files found.")

    except Exception as e:
        print("Error listing files:", e)


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":

    BUCKET_NAME = "aws-storage-project-bucket"
    REGION = "ap-south-1"

    S3_KEY = "small_file.csv"                  # File in S3
    LOCAL_FILE = "downloaded_sample.csv"   # Local file name

    # Download
    success = download_file(BUCKET_NAME, S3_KEY, LOCAL_FILE, REGION)

    # Verify by Size
    if success and os.path.exists(LOCAL_FILE):
        verify_by_size(BUCKET_NAME, S3_KEY, LOCAL_FILE, REGION)

    # List Files 
    list_files(BUCKET_NAME, prefix="", region=REGION)