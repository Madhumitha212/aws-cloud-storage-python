import boto3
import os
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from boto3.s3.transfer import TransferConfig

# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# Create S3 Client
# ---------------------------
def create_s3_client(region_name):
    try:
        return boto3.client("s3", region_name=region_name)
    except (NoCredentialsError, PartialCredentialsError):
        logging.error("AWS credentials not found or invalid.")
        raise

# ---------------------------
# Upload file (small or large)
# ---------------------------
def upload_file(file_path, bucket_name, region_name, s3_key=None):
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return False

    if not s3_key:
        s3_key = os.path.basename(file_path)

    try:
        s3_client = create_s3_client(region_name)
        s3_client.head_bucket(Bucket=bucket_name)

        config = TransferConfig(
            multipart_threshold=5*1024*1024,  # 5 MB
            max_concurrency=4,
            multipart_chunksize=5*1024*1024,
            use_threads=True
        )

        logging.info(f"Uploading '{file_path}' to bucket '{bucket_name}' as '{s3_key}'...")
        s3_client.upload_file(file_path, bucket_name, s3_key, Config=config)
        logging.info("Upload successful.")
        return True

    except NoCredentialsError:
        logging.error("Invalid AWS credentials.")
    except PartialCredentialsError:
        logging.error("Incomplete AWS credentials.")
    except ClientError as e:
        code = e.response['Error']['Code']
        if code == "404":
            logging.error(f"Bucket '{bucket_name}' does not exist.")
        elif code == "403":
            logging.error(f"Access denied to bucket '{bucket_name}'.")
        else:
            logging.error(f"AWS ClientError: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return False

# ---------------------------
# Download file
# ---------------------------
def download_file(bucket_name, s3_key, local_path, region):
    folder = os.path.dirname(local_path) 
    if folder: 
        os.makedirs(folder, exist_ok=True)
    try:
        s3 = create_s3_client(region)
        logging.info(f"Downloading '{s3_key}' from bucket '{bucket_name}'...")
        s3.download_file(bucket_name, s3_key, local_path)
        logging.info(f"Downloaded successfully to '{local_path}'")
        return True
    except NoCredentialsError:
        logging.error("AWS credentials not found.")
    except ClientError as e:
        logging.error(f"AWS Client Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return False

# ---------------------------
# Verify file integrity by size
# ---------------------------
def verify_by_size(bucket_name, s3_key, local_path, region):
    try:
        s3 = create_s3_client(region)
        response = s3.head_object(Bucket=bucket_name, Key=s3_key)
        s3_size = response["ContentLength"]
        local_size = os.path.getsize(local_path)

        logging.info(f"Verifying integrity for '{s3_key}'...")
        logging.info(f"S3 file size   : {s3_size} bytes")
        logging.info(f"Local file size: {local_size} bytes")

        if s3_size == local_size:
            logging.info("File integrity verified.")
        else:
            logging.warning("Integrity mismatch detected!")

    except Exception as e:
        logging.error(f"Verification error: {e}")

# ---------------------------
# List files in bucket/prefix
# ---------------------------
def list_files(bucket_name, prefix, region):
    try:
        s3 = create_s3_client(region)
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        logging.info(f"Listing files in bucket '{bucket_name}' with prefix '{prefix}'...")

        if "Contents" in response:
            for obj in response["Contents"]:
                logging.info(obj["Key"])
        else:
            logging.info("No files found.")
    except Exception as e:
        logging.error(f"Error listing files: {e}")