# AWS Storage with RDS Data Pipeline Using Python

## Project Overview

This project demonstrates integration between **Python (Boto3, Pandas, PyODBC)** and **AWS services (S3 and RDS)** to build a secure, cloud-based data pipeline.

The pipeline performs:

- Uploading raw datasets to Amazon S3
- Cleaning and transforming data using Python
- Storing processed data back in S3
- Inserting structured data into Amazon RDS
- Running SQL analytics
- Exporting results to CSV files

---

## Development Environment

| Component | Details |
|-----------|---------|
| OS | Windows with WSL (Ubuntu) |
| Cloud Environment | AWS EC2 (Ubuntu) |
| Programming Language | Python 3.x |
| AWS SDK | Boto3 |
| Database Connectivity | PyODBC |
| Data Processing | Pandas |

All commands were executed inside the **WSL terminal** or **EC2 instance**.

---

## AWS Services Used

### Amazon S3
Used for storing datasets in two stages:

- Raw data
- Processed data

### Amazon RDS
Used to store structured data and perform SQL analytics.

### Amazon EC2
Runs the pipeline scripts in a cloud environment using IAM role authentication.

### IAM (Identity and Access Management)

Used to securely configure access.

Two authentication methods were used:

- **IAM User** for WSL using `aws configure`
- **IAM Role** attached to EC2 instance

---

## AWS CLI Configuration

AWS CLI installation is handled automatically using the **setup.sh script**.

Before running the project, configure AWS credentials for your IAM user.

Run the following command:

```bash
aws configure
```

Enter the required credentials:

```
AWS Access Key ID: <your-access-key>
AWS Secret Access Key: <your-secret-key>
Default region name: <your-region>
Default output format: json
```

Example:

```
AWS Access Key ID: AKIA*************
AWS Secret Access Key: *********************
Default region name: us-east-1
Default output format: json
```

These credentials are securely stored in:

```
~/.aws/credentials
```

### Test the Configuration

To verify that AWS CLI is configured correctly, run:

```bash
aws s3 ls
```

If configured successfully, it will display the list of S3 buckets in your AWS account.

---

## Project Structure

```
aws_storage_with_rds/
│
├── datasets/
│   └── sales_transactions.csv
│
├── documents/
│   ├── aws_concepts.txt
│   └── aws_provisioning.txt
│
├── config/
|   ├── connection.py
|   └── s3_config.py
│
├── scripts/
│   ├── data_ingestion.py
│   ├── data_cleaning_transformation.py
|   ├── download_processed.py
│   ├── insertion.py
│   ├── sql_analytics.py
│   └── export_to_csv.py
│
├── setup/
|   ├── setup_console.txt
|   ├── setup_ec2.sh
|   └── setup_wsl.sh
|
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Running the Project (WSL)

1.Open WSL

2.Install dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

3.Clone the repository

```bash
git clone <>
cd aws_storage_with_rds
```

4.Run the setup script (installs dependencies including AWS CLI):

```bash
bash setup_wsl.sh
```

Configure AWS credentials:

```bash
aws configure
```

Run the pipeline scripts in sequence:

```bash
python -m scripts.data_ingestion
python -m scripts.data_cleaning_transformation
python -m scripts.download_processed
python -m scripts.insertion
python -m scripts.sql_analytics
python -m scripts.export_to_csv
```

---

## Script Description

### data_ingestion.py

- Reads raw dataset from local system
- Uploads dataset to **S3 raw folder**

### data_cleaning_transformation.py

- Cleans dataset using **Pandas**
- Handles missing values and formatting
- Saves processed dataset locally
- Uploads cleaned data to **S3 processed folder**

### insertion.py

- Connects to **Amazon RDS** using PyODBC
- Creates database tables
- Inserts cleaned dataset into RDS

### sql_analytics.py

Runs SQL queries to analyze data such as:

- Total sales
- Product-wise sales
- Aggregations and grouping

### export_to_csv.py

- Extracts query results from **RDS**
- Saves analytics output as **CSV files**

---

## Security Best Practices

The following security practices were followed:

- AWS credentials are **not stored in source code**
- Authentication managed through **AWS CLI**
- IAM roles used for **EC2 access**
- Minimal permissions granted to IAM users
- Modular and reusable script structure

---

## Running the Project on EC2

1. Launch an **Ubuntu EC2 instance (Free Tier)**

2. Attach an **IAM Role** with access to:
   - Amazon S3
   - Amazon RDS

3. Install dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

4. Clone the repository

```bash
git clone <>
cd aws_storage_with_rds
```

5. Run setup script

```bash
bash setup_ec2.sh
```

6. Execute the pipeline

```bash
python -m scripts.data_ingestion
python -m scripts.data_cleaning_transformation
python -m scripts.download_processed
python -m script.insertion
python -m scripts.sql_analytics
python -m scripts.export_to_csv
```

---

## Assumptions

- AWS Free Tier account is available
- IAM permissions are configured correctly
- AWS CLI is configured
- Internet connectivity is available
- Python dependencies are installed

---

## Author

**R Madhumitha**
