import pandas as pd
from config.connection import *
from config.s3_config import *

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

def insert_data(conn):
    # Load CSV
    df = pd.read_csv(LOCAL_PROCESS_DOWNLOAD_PATH)

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

    cursor.fast_executemany = True
    cursor.executemany(insert_query, df.values.tolist())

    conn.commit()

    print("Data inserted successfully!")

if __name__ == "__main__":

    conn = get_connection()
    create_table_if_not_exists(conn)
    insert_data(conn)
    conn.close()