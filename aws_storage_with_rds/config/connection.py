#configurations to connect to RDS
import pyodbc

RDS_DRIVER = "{ODBC Driver 17 for SQL Server}"
RDS_SERVER = "aws-project-database.c94iqcqk2mie.ap-south-1.rds.amazonaws.com,1433;"
RDS_DATABASE = "transactiondb"
RDS_USERNAME = "admin"
RDS_PASSWORD = "_Bhanu123_"

def get_connection():
    return pyodbc.connect(
        f"DRIVER={RDS_DRIVER};"
        f"SERVER={RDS_SERVER};"
        f"DATABASE={RDS_DATABASE};"
        f"UID={RDS_USERNAME};"
        f"PWD={RDS_PASSWORD}"
    )