#!/bin/bash
# EC2 setup script for AWS Storage & RDS project
# Assumes IAM role is attached to EC2 instance (no aws configure needed)

set -e

echo " Updating system packages..."
sudo apt update -y

echo " Installing core dependencies..."
sudo apt install -y python3-pip python3-venv unixodbc unixodbc-dev curl

# --- Install Microsoft ODBC Driver (msodbcsql17) if not present ---
if ! odbcinst -q -d | grep -q "ODBC Driver 17 for SQL Server"; then
    echo "Installing Microsoft ODBC Driver 17..."
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
    sudo apt update -y
    sudo ACCEPT_EULA=Y apt install -y msodbcsql17
else
    echo " ODBC Driver 17 already installed."
fi

# --- Setup Python virtual environment ---
if [ ! -d "venv" ]; then
    echo " Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo " Activating virtual environment..."
source venv/bin/activate

# --- Install Python dependencies ---
echo " Installing Python packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "EC2 setup complete!"
echo "Next steps:"
echo "1. Run 'source venv/bin/activate' to activate your environment."
echo "2. Ensure your EC2 instance has an IAM role with S3 + RDS permissions."
echo "3. Execute your scripts in order: data_ingestion.py → data_cleaning_transformation.py → insertion.py → sql_analytics.py → export_to_csv.py"
