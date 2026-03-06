import os
from botocore.exceptions import NoCredentialsError, ClientError
import config.s3_config as s3_config


def upload_file_to_s3(local_file, bucket, s3_key):
    """Upload a file to S3."""
    s3 = s3_config.get_s3_client()
    try:
        s3.upload_file(local_file, bucket, s3_key)
        print(f"Uploaded {local_file} to s3://{bucket}/{s3_key}")

    except FileNotFoundError:
        print("Local file not found.")

    except NoCredentialsError:
        print("AWS credentials not available.")

    except ClientError as e:
        print(f"Upload failed: {e}")


def list_files_in_s3(bucket, prefix=""):
    """List files in S3 under a given prefix."""
    s3 = s3_config.get_s3_client()

    try:
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix
        )

        if "Contents" in response:
            print(f"Files under {prefix}:")

            for obj in response["Contents"]:
                print(obj["Key"])

        else:
            print("No files found.")

    except ClientError as e:
        print(f"Listing failed: {e}")


def download_file_from_s3(bucket, s3_key, local_path):
    """Download a file from S3."""

    s3 = s3_config.get_s3_client()

    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        s3.download_file(
            bucket,
            s3_key,
            local_path
        )

        print(f"Downloaded s3://{bucket}/{s3_key} to {local_path}")

    except ClientError as e:
        print(f"Download failed: {e}")


if __name__ == "__main__":

    bucket = s3_config.S3_BUCKET_NAME

    # Define files here (NOT in config)
    local_file = "dataset/sales_transactions.csv"
    s3_key = "raw/sales_transactions.csv"
    download_path = "downloads/sales_transactions.csv"

    # Upload
    upload_file_to_s3(local_file, bucket, s3_key)

    # List
    list_files_in_s3(bucket)

    # Download
    download_file_from_s3(bucket, s3_key, download_path)