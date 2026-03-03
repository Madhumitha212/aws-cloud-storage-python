import os
from botocore.exceptions import NoCredentialsError, ClientError
import config

def upload_file_to_s3(local_file, bucket, s3_key):
    """Upload a file to S3."""
    s3 = config.get_s3_client()
    try:
        s3.upload_file(local_file, bucket, s3_key)
        print(f" Uploaded {local_file} to s3://{bucket}/{s3_key}")
    except FileNotFoundError:
        print(" Local file not found.")
    except NoCredentialsError:
        print(" AWS credentials not available.")
    except ClientError as e:
        print(f" Upload failed: {e}")

def list_files_in_s3(bucket, prefix=""):
    """List files in S3 under a given prefix."""
    s3 = config.get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if "Contents" in response:
            print(f" Files under {prefix}:")
            for obj in response["Contents"]:
                print(f" - {obj['Key']}")
        else:
            print(" No files found.")
    except ClientError as e:
        print(f" Listing failed: {e}")

def download_file_from_s3(bucket, s3_key, local_path):
    """Download a file from S3."""
    s3 = config.get_s3_client()
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        s3.download_file(bucket, s3_key, local_path)
        print(f" Downloaded s3://{bucket}/{s3_key} to {local_path}")
    except ClientError as e:
        print(f" Download failed: {e}")


if __name__ == "__main__":
    # Example workflow
    s3_key = config.S3_RAW_PREFIX + os.path.basename(config.LOCAL_RAW_FILE)

    # Upload raw dataset
    upload_file_to_s3(config.LOCAL_RAW_FILE, config.S3_BUCKET_NAME, s3_key)

    # List files in raw folder
    list_files_in_s3(config.S3_BUCKET_NAME, config.S3_RAW_PREFIX)

    # Download file back
    download_file_from_s3(config.S3_BUCKET_NAME, s3_key, config.LOCAL_DOWNLOAD_PATH)
