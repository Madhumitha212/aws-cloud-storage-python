import pandas as pd
from config.connection import *
from config.s3_config import *

def insert_data():
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
    conn = get_connection()
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
    conn.close()

    print("Data inserted successfully!")

if __name__ == "__main__":
    insert_data()