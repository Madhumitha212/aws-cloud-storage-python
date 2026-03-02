# AWS Cloud and Storage Integration Using Python (Boto3)

## Project Overview

This project demonstrates integration between Python (Boto3 SDK) and Amazon S3 for secure cloud-based file transfer.

The implementation was developed and executed inside **WSL (Windows Subsystem for Linux)**, simulating a Linux-based cloud development environment.

The system supports:

- Uploading files (small and large) to S3
- Downloading files from S3
- Listing bucket contents
- Error handling for real-world cloud scenarios
- Modular and automated execution
- Secure IAM-based authentication

---

## Development Environment

- OS: Windows with WSL (Ubuntu)
- Python Version: Python 3.x
- AWS CLI configured inside WSL
- Boto3 SDK for AWS interaction

All commands were executed inside the WSL terminal.

---

## AWS Services Used

### 1. Amazon S3 (Simple Storage Service)
Used for secure object storage and file transfer.

### 2. Amazon EC2 (Conceptual + Execution)
Explained how the same scripts can run inside an EC2 instance.

### 3. IAM (Identity and Access Management)
Used to securely configure:
- IAM User
- Access Keys
- IAM Roles (for EC2 usage)

---

## Cloud Concepts Covered

### What is Cloud Computing?

Cloud computing provides on-demand computing resources such as servers, storage, and networking over the internet with pay-as-you-go pricing.

---

### IaaS vs PaaS vs SaaS

| Model | Description | Example |
|--------|------------|----------|
| IaaS | Infrastructure as a Service | Amazon EC2 |
| PaaS | Platform as a Service | AWS Elastic Beanstalk |
| SaaS | Software as a Service | Gmail |

---

##  Project Structure

```
aws_cloud_storage_integration/
│
├── datasets/
│   └── small_file.csv
│
├── documents/
│   ├── aws_setup.txt
│   ├── cloud_aws_understanding.txt
│   └── ec2_context.txt
│
├── downloads/
│   └── small_file.csv
│
├── source/
│   ├── automation.py
│   ├── automation_main.py
│   ├── config.py
│   ├── upload.py
│   └── download.py
│
├── requirements.txt
└── README.md
```

---

## Running the Project (Inside WSL)

Navigate to project directory:

```bash
cd aws_cloud_storage_integration
```

Run the main automation script:

```bash
python3 source/automation_main.py
```

---

## Script Explanation

### upload.py
- Uploads files from `datasets/` folder to S3
- Handles:
  - FileNotFoundError
  - NoCredentialsError
  - ClientError (invalid bucket / permission)

---

### download.py
- Downloads files from S3
- Stores them inside `downloads/`
- Verifies successful download

---

### automation.py
- Contains reusable S3 functions
- Handles S3 client initialization
- Implements structured error handling

---

### automation_main.py
- Main execution entry point
- Calls upload and download functions
- Uses parameters from config.py

---

### config.py
- Stores:
  - Bucket name
  - Region
  - File paths
- Avoids hardcoding configuration inside business logic

---

## Security Best Practices Followed

- AWS credentials stored using AWS CLI (not in code)
- IAM user configured with limited S3 permissions
- Code structured for IAM Role compatibility (for EC2)

---

## Running the Same Script on EC2 

If deployed on EC2:

1. Launch EC2 instance (Free Tier)
2. Attach IAM Role with S3 access
3. Install Python and Boto3
4. Run the same script

---

## Assumptions

- AWS Free Tier account used
- Proper IAM permissions configured
- Internet connectivity available
- WSL properly installed and configured

---

## Author

R Madhumitha  