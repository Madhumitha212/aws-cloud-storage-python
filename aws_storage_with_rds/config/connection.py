#configurations to connect to RDS
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

RDS_DRIVER = os.getenv("RDS_DRIVER")
RDS_SERVER = os.getenv("RDS_SERVER")
RDS_DATABASE = os.getenv("RDS_DATABASE")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")

def get_connection():
    return pyodbc.connect(
        f"DRIVER={RDS_DRIVER};"
        f"SERVER={RDS_SERVER};"
        f"DATABASE={RDS_DATABASE};"
        f"UID={RDS_USERNAME};"
        f"PWD={RDS_PASSWORD}"
    )