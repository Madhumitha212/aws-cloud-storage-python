import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from boto3.s3.transfer import TransferConfig

# ----------------------------
# Create S3 Client
# ----------------------------
def create_s3_client(region_name):
    try:
        s3_client = boto3.client("s3", region_name=region_name)
        return s3_client
    except (NoCredentialsError, PartialCredentialsError):
        print("Error: AWS credentials not found or invalid.")
        raise

# ----------------------------
# Upload File Function
# ----------------------------
def upload_file(file_path, bucket_name, region_name, s3_key=None):

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False

    if not s3_key:
        s3_key = os.path.basename(file_path)

    try:
        s3_client = create_s3_client(region_name)

        # Check if bucket exists and accessible
        s3_client.head_bucket(Bucket=bucket_name)

        # Configure multipart threshold (for large files)
        config = TransferConfig(
            multipart_threshold=5 * 1024 * 1024,  # 5MB
            max_concurrency=4,
            multipart_chunksize=5 * 1024 * 1024,
            use_threads=True
        )

        print(f"Uploading {file_path} to bucket {bucket_name}...")

        s3_client.upload_file(
            file_path,
            bucket_name,
            s3_key,
            Config=config
        )

        print("Upload successful.")
        return True

    except NoCredentialsError:
        print("Error: Invalid AWS credentials.")
        return False

    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
        return False

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "404":
            print(f"Error: Bucket '{bucket_name}' does not exist.")
        elif error_code == "403":
            print(f"Error: Access denied to bucket '{bucket_name}'.")
        else:
            print(f"AWS ClientError: {e}")

        return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":

    # Parameters (can be changed easily)
    BUCKET_NAME = "aws-storage-project-bucket"
    REGION = "ap-south-1"

    # Small file upload
    upload_file("/mnt/d/aws_cloud_storage/datasets/small_file.csv", BUCKET_NAME, REGION)

    # Large file upload
    upload_file("/mnt/d/aws_cloud_storage/datasets/large_file.log", BUCKET_NAME, REGION)