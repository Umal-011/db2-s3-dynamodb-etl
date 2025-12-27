import ibm_db
import boto3
import csv
import io

# ---------------- DB2 CONNECTION ----------------
conn_str = (
    "DATABASE=testdb;"
    "HOSTNAME=localhost;"
    "PORT=50000;"
    "PROTOCOL=TCPIP;"
    "UID=db2inst1;"
    "PWD=db2inst1;"
)

conn = ibm_db.connect(conn_str, "", "")

sql = "SELECT ID, NAME, MARKS FROM STUDENT"
stmt = ibm_db.exec_immediate(conn, sql)

# ---------------- IN-MEMORY CSV ----------------
csv_buffer = io.StringIO()
writer = csv.writer(csv_buffer)

# Header
writer.writerow(["ID", "NAME", "MARKS"])

row = ibm_db.fetch_assoc(stmt)
while row:
    writer.writerow([row["ID"], row["NAME"], row["MARKS"]])
    row = ibm_db.fetch_assoc(stmt)

# ---------------- UPLOAD TO S3 ----------------
s3 = boto3.client("s3", region_name="us-east-1")

BUCKET_NAME = "s3-bucket-uma-2025"
S3_KEY = "student/student_data.csv"

s3.put_object(
    Bucket=BUCKET_NAME,
    Key=S3_KEY,
    Body=csv_buffer.getvalue()
)

print("✅ DB2 data successfully uploaded to S3 as CSV")
