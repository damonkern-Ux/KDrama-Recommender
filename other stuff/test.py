import unicodedata
import re
import csv
import mysql.connector as mysql
import json
def normalize_title(s):
    # 1. Unicode normalize (so fullwidth chars → normal ones)
    s = unicodedata.normalize("NFKC", s)
    # 2. Strip leading/trailing whitespace
    s = s.strip()
    # 3. Remove non-breaking spaces
    s = s.replace("\u00a0", " ")
    # 4. Collapse multiple spaces → one space
    s = re.sub(r"\s+", " ", s)
    # 5. Ensure slash spacing is consistent: " / "
    s = re.sub(r"\s*/\s*", " / ", s)
    s = s.split("/")[-1].strip()
    s = s.title()
    return s
connection = mysql.connect(
    user="root", password="system", host="localhost", charset="utf8mb4"
)
data=[]
cursor = connection.cursor()
cursor.execute("USE dramas;")
cursor.execute("SELECT drama_name FROM drama_table;")
drama_table = cursor.fetchall()
for name in drama_table:
    name = normalize_title(name[0])
    data.append(name.lower())
data.sort()

viki = []
with open ("./other stuff/Viki.csv","r",newline='') as file:
    reader = csv.reader(file)
    for i in reader:
        viki.append((i[0].lower(),i[1].lower()))


filex = open("./other stuff/dramas.csv","w",newline='')
writer = csv.writer(filex)
for name in data:
    for search in viki:
        writer.writerow((name,search))
        if name.lower() == search[0] or name.lower() == search[1]: 
            print("found",name)
            cursor.execute("SELECT platform FROM drama_table WHERE LOWER(drama_name) LIKE %s",(f"%{name}%",))
            platform = json.loads(cursor.fetchall()[0][0])
            platform = (platform + ", Viki") if platform != "None" else "Viki"
            cursor.execute("UPDATE drama_table SET platform = %s WHERE LOWER(drama_name) LIKE %s",(json.dumps(platform),f"%{name}%"))
            break
filex.close()
connection.commit()
cursor.close()
connection.close()