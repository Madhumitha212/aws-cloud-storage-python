#!/bin/bash

# Exit immediately if a command fails
set -e

echo "Updating system packages..."
sudo apt update -y

# --- Install AWS CLI if not present ---
if ! command -v aws &> /dev/null
then
    echo "Installing AWS CLI..."
    sudo apt install -y awscli
else
    echo "AWS CLI already installed."
fi

# --- Install unixODBC if not present ---
if ! dpkg -s unixodbc &> /dev/null
then
    echo "Installing unixODBC..."
    sudo apt install -y unixodbc unixodbc-dev
else
    echo "unixODBC already installed."
fi

# --- Install Microsoft ODBC Driver (msodbcsql17) if not present ---
if ! odbcinst -q -d | grep -q "ODBC Driver 17 for SQL Server"
then
    echo " Installing Microsoft ODBC Driver 17..."
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
    sudo apt update -y
    sudo ACCEPT_EULA=Y apt install -y msodbcsql17
else
    echo "ODBC Driver 17 already installed."
fi

# --- Setup Python virtual environment ---
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source venv/bin/activate

# --- Install Python dependencies ---
echo "Installing Python packages from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete!"
echo "Next steps:"
echo "1. Run 'source venv/bin/activate' to activate your environment."
echo "2. Configure AWS CLI with 'aws configure' (if not already done)."
echo "3. Execute your scripts in order: data_ingestion.py → data_cleaning_transformation.py → insertion.py → sql_analytics.py → export_to_csv.py"
