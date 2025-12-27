import boto3
import csv
import io

# AWS clients
s3 = boto3.client("s3", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

# Resources
BUCKET_NAME = "s3-bucket-uma-2025"
S3_KEY = "student/student_data.csv"
TABLE_NAME = "Student"

table = dynamodb.Table(TABLE_NAME)

# Read CSV from S3
response = s3.get_object(Bucket=BUCKET_NAME, Key=S3_KEY)
csv_content = response["Body"].read().decode("utf-8")

csv_reader = csv.DictReader(io.StringIO(csv_content))

# Insert into DynamoDB
for row in csv_reader:
    # Skip empty or invalid rows
    if not row["ID"] or not row["MARKS"]:
        continue

    table.put_item(
        Item={
            "ID": int(row["ID"].strip()),
            "NAME": row["NAME"].strip(),
            "MARKS": int(row["MARKS"].strip())
        }
    )


print("✅ Data successfully migrated from S3 to DynamoDB")
