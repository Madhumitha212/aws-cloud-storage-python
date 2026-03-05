import os
import pandas as pd
from config.connection import *


def export_to_csv():
    conn = get_connection()
    cursor = conn.cursor()

    # Run query
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    print("Rows fetched:", len(rows))

    # Get column names directly from cursor
    columns = [desc[0] for desc in cursor.description]

    # Convert to DataFrame
    df = pd.DataFrame.from_records(rows, columns=columns)

    # Ensure directory exists
    output_dir = "/mnt/d/aws_cloud_storage/aws_storage_with_rds/downloads"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "exported_results.csv")

    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Data exported successfully! Rows: {len(df)} File: {output_path}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    export_to_csv()

# 3. Explain different methods for bulk import/export

# 1. Using SQL Server Management Studio (SSMS) for SQL Server: 
#   This tool provides a graphical interface for importing and exporting 
#   data using the Import and Export Wizard.

# 2. Using BCP (Bulk Copy Program): This is a command-line tool that allows 
#   for fast import and export of data between SQL Server and other data 
#   sources.Very fast handles millions of data.

# 3. Using Python libraries like pandas and pyodbc: This method allows for 
#   programmatic control over the import and export process, making it 
#   suitable for automation and integration into data pipelines.
