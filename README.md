# DB2 → S3 → DynamoDB Migration

This project provides scripts to migrate data from a CSV file to DB2, then to AWS S3, and finally to DynamoDB.

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Access to a DB2 database
- AWS account with S3 and DynamoDB permissions
- AWS CLI configured (`aws configure`)

## Setup

1. **Clone the repository**

```bash
git clone <repo-url>
cd db2_s3_dynamodb
```

2. **Install required Python packages**

```bash
pip install ibm-db boto3 pandas
```

- `ibm-db`: For DB2 connectivity
- `boto3`: For AWS S3 and DynamoDB operations
- `pandas`: For CSV handling

3. **Configure AWS CLI**

```bash
aws configure
```

Enter your AWS Access Key, Secret Key, region, and output format.

## Migration Steps

### 1. Load CSV to DB2

Edit `db2_to_s3.py` or `migrate.py` to set your DB2 connection details and CSV file path.

Run:

```bash
python db2_to_s3.py
```

### 2. Export Data from DB2 to S3

Ensure your DB2 credentials and S3 bucket details are set in the script.

Run:

```bash
python db2_to_s3.py
```

This will extract data from DB2 and upload it to your specified S3 bucket.

### 3. Move Data from S3 to DynamoDB

Edit `s3_to_dynamodb.py` to set your S3 bucket and DynamoDB table details.

Run:

```bash
python s3_to_dynamodb.py
```

This will download the data from S3 and insert it into DynamoDB.

### 4. Compare DB2 and DynamoDB (Optional)

To verify data consistency:

```bash
python compare_db2_dynamodb.py
```

## File Descriptions

- `student.csv`: Sample CSV data
- `db2_to_s3.py`: Script to move data from DB2 to S3
- `s3_to_dynamodb.py`: Script to move data from S3 to DynamoDB
- `compare_db2_dynamodb.py`: Script to compare DB2 and DynamoDB data
- `migrate.py`: (If present) End-to-end migration script

## Notes

- Update all scripts with your actual DB2, S3, and DynamoDB details before running.
- Ensure your AWS credentials have the necessary permissions.

## Troubleshooting

- Check Python and package versions if you encounter errors.
- Ensure network access to DB2 and AWS services.

---

For any issues, please raise an issue or contact the maintainer.
