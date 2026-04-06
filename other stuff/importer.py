import csv
import json
import mysql.connector as mysql

connection = mysql.connect(
    host="localhost",
    user="root",
    password="system",
    database="dramas",
    charset="utf8mb4",
    use_unicode=True,
)
connection.set_charset_collation('utf8mb4', 'utf8mb4_unicode_ci')
cursor = connection.cursor()
cursor.execute("SET NAMES utf8mb4;")
cursor.execute("SET CHARACTER SET utf8mb4;")
cursor.execute("SET character_set_connection=utf8mb4;")
with open(
    "D:\\Archalanthera\\Projects\\KDrama-Recommender\\data.csv", "r", encoding="utf-8"
) as file:
    reader = csv.reader(file)
    for row in reader:
        insert = []
        insert.append(row[0].strip())
        insert.append(int(row[1]))
        insert.append(int(row[2]))
        insert.append(row[3])
        insert.append(row[4])
        insert.append(row[5].replace('"', "").strip())
        insert.append(float(row[6]))
        insert.append(row[7].replace("[", "").replace("]", "").replace('"', ""))
        values = (
            insert[0],
            insert[1],
            insert[2],
            insert[3],
            insert[4],
            json.dumps(insert[5]),
            insert[6],
            json.dumps(insert[7]),
        )
        query = """
INSERT INTO Drama_Table (
    Drama_Name,
    Year,
    Episodes_Number,
    Description,
    Cast,
    Tags,
    Rating,
    Platform
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
        cursor.execute(query, values)

connection.commit()
cursor.close()
connection.close()
