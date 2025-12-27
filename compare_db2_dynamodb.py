import ibm_db
import boto3

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

db2_data = {}

row = ibm_db.fetch_assoc(stmt)
while row:
    if row["ID"] is None or row["MARKS"] is None:
        row = ibm_db.fetch_assoc(stmt)
        continue

    db2_data[int(row["ID"])] = {
        "NAME": (row["NAME"] or "").strip(),
        "MARKS": int(row["MARKS"])
    }

    row = ibm_db.fetch_assoc(stmt)


print(f"✅ DB2 records loaded: {len(db2_data)}")

# ---------------- DYNAMODB CONNECTION ----------------
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("Student")

response = table.scan()
items = response.get("Items", [])

# Handle pagination (important for real tables)
while "LastEvaluatedKey" in response:
    response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
    items.extend(response["Items"])

ddb_data = {}

for item in items:
    if "ID" not in item or "MARKS" not in item:
        continue

    if item["ID"] is None or item["MARKS"] is None:
        continue

    ddb_data[int(item["ID"])] = {
        "NAME": (item.get("NAME") or "").strip(),
        "MARKS": int(item["MARKS"])
    }

print(f"✅ DynamoDB records loaded: {len(ddb_data)}")

# ---------------- COMPARISON ----------------
missing_in_ddb = []
missing_in_db2 = []
mismatched_records = []

# Check DB2 → DynamoDB
for emp_id, db2_row in db2_data.items():
    if emp_id not in ddb_data:
        missing_in_ddb.append(emp_id)
    else:
        if db2_row != ddb_data[emp_id]:
            mismatched_records.append({
                "ID": emp_id,
                "DB2": db2_row,
                "DynamoDB": ddb_data[emp_id]
            })

# Check DynamoDB → DB2
for emp_id in ddb_data:
    if emp_id not in db2_data:
        missing_in_db2.append(emp_id)

# ---------------- REPORT ----------------
print("\n========== VALIDATION REPORT ==========")

if not missing_in_ddb and not missing_in_db2 and not mismatched_records:
    print("🎉 SUCCESS: DB2 and DynamoDB data MATCH exactly")
else:
    if missing_in_ddb:
        print(f"❌ Missing in DynamoDB: {missing_in_ddb}")

    if missing_in_db2:
        print(f"❌ Missing in DB2: {missing_in_db2}")

    if mismatched_records:
        print("\n⚠️ Mismatched Records:")
        for rec in mismatched_records:
            print(rec)

print("======================================")










