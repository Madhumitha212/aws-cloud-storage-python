import csv
from io import StringIO
from config.s3_config import get_s3_client, S3_BUCKET_NAME   # adjust import if needed


def upload_query_results_to_s3(file_name, rows, headers):
    
    s3 = get_s3_client()

    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)

    writer.writerow(headers)
    writer.writerows(rows)

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        Body=csv_buffer.getvalue()
    )

    print(f"{file_name} uploaded successfully to {S3_BUCKET_NAME}")