import automation
import config
import os

def main():
    # ---------------------------
    # Upload small file
    # ---------------------------
    automation.upload_file(
        config.LOCAL_SMALL_FILE,
        config.BUCKET_NAME,
        config.AWS_REGION,
        config.S3_SMALL_KEY
    )

    # ---------------------------
    # Upload large file
    # ---------------------------
    automation.upload_file(
        config.LOCAL_LARGE_FILE,
        config.BUCKET_NAME,
        config.AWS_REGION,
        config.S3_LARGE_KEY
    )

    # ---------------------------
    # List all files
    # ---------------------------
    automation.list_files(config.BUCKET_NAME, prefix="", region=config.AWS_REGION)

    # ---------------------------
    # Download small file
    # ---------------------------
    automation.download_file(
        config.BUCKET_NAME,
        config.S3_SMALL_KEY,
        config.LOCAL_DOWNLOAD_SMALL,
        config.AWS_REGION
    )

    # ---------------------------
    # Download large file
    # ---------------------------
    automation.download_file(
        config.BUCKET_NAME,
        config.S3_LARGE_KEY,
        config.LOCAL_DOWNLOAD_LARGE,
        config.AWS_REGION
    )

    # ---------------------------
    # Verify small file
    # ---------------------------
    automation.verify_by_size(
        config.BUCKET_NAME,
        config.S3_SMALL_KEY,
        config.LOCAL_DOWNLOAD_SMALL,
        config.AWS_REGION
    )

    # ---------------------------
    # Verify large file
    # ---------------------------
    automation.verify_by_size(
        config.BUCKET_NAME,
        config.S3_LARGE_KEY,
        config.LOCAL_DOWNLOAD_LARGE,
        config.AWS_REGION
    )

if __name__ == "__main__":
    os.makedirs("download", exist_ok=True)
    main()