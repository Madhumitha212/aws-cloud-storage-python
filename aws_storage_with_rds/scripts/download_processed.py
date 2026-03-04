import os
from config.s3_config import *
from botocore.exceptions import *

def download_file(bucket, s3_key, local_path):
    """Download a file from S3."""
    s3 = get_s3_client()
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        s3.download_file(bucket, s3_key, local_path)
        print(f" Downloaded s3://{bucket}/{s3_key} to {local_path}")
    except ClientError as e:
        print(f" Download failed: {e}")

if __name__ == "__main__":
    s3_process_key = S3_PROCESSED_PREFIX + os.path.basename(PROCESSED_PATH)

    download_file(S3_BUCKET_NAME, s3_process_key, LOCAL_PROCESS_DOWNLOAD_PATH)