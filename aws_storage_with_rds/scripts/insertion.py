import pandas as pd
from io import StringIO
from config.connection import *
import config.s3_config as s3_config
import pyodbc  # assuming you use pyodbc

def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    create_table_query = """
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'transactions')
    BEGIN
        CREATE TABLE transactions(
            transaction_id VARCHAR(20) PRIMARY KEY,
            transaction_date DATETIME,
            customer_id VARCHAR(10), 
            product_id VARCHAR(10),
            region VARCHAR(20),
            quantity INT, 
            price_per_unit DECIMAL(10, 2), 
            total_amount DECIMAL(10, 2),
            discount_percent DECIMAL(10,2), 
            final_amount DECIMAL(10,2)
        )
    END
    """
    cursor.execute(create_table_query)
    conn.commit()


def read_csv_from_s3(file_key):
    s3 = s3_config.get_s3_client()
    response = s3.get_object(
        Bucket=s3_config.S3_BUCKET_NAME,
        Key=file_key
    )
    csv_data = response["Body"].read().decode("utf-8")
    df = pd.read_csv(StringIO(csv_data))
    return df


def insert_data(conn, file_key):
    df = read_csv_from_s3(file_key)

    required_columns = [
        "transaction_id",
        "transaction_date",
        "customer_id",
        "product_id",
        "region",
        "quantity",
        "price_per_unit",
        "total_amount",
        "discount_percent",
        "final_amount"
    ]
    df = df[required_columns]
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO transactions (
        transaction_id, transaction_date, customer_id,
        product_id, region, quantity,
        price_per_unit, total_amount,
        discount_percent, final_amount
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.fast_executemany = True
        cursor.executemany(insert_query, df.values.tolist())
        conn.commit()
        print("Data inserted successfully!")
    except pyodbc.IntegrityError as e:
        # This error occurs if transaction_id already exists
        print("Error: Some rows already exist in the database. Aborting insert.")
        raise e  # re-raise the exception to stop execution


if __name__ == "__main__":
    conn = get_connection()
    create_table_if_not_exists(conn)
    insert_data(conn, "processed/cleaned_sales.csv")
    conn.close()