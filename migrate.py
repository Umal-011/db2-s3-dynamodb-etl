import csv

with open('student.csv', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
