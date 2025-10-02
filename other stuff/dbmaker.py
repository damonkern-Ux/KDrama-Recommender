import csv
import mysql.connector as mysql
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import math

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


# Connect to MySQL
def table_maker():
    connection = mysql.connect(
        user="root", password="system", host="localhost", charset="utf8mb4"
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS dramas;")
    cursor.execute("USE dramas;")
    cursor.execute("DROP TABLE IF EXISTS User_Table;")
    cursor.execute("DROP TABLE IF EXISTS Drama_Table;")
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS Drama_Table (
    Drama_Name VARCHAR(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci PRIMARY KEY,
    Year INT(4),
    Episodes_Number INT(3),
    Description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Cast JSON,
    Tags JSON,
    Rating FLOAT,
    Platform JSON
) ENGINE=InnoDB;
"""
    )
    print("Drama_Table created successfully!")
    cursor.execute(
        """
CREATE TABLE IF NOT EXISTS User_Table (
    Drama_Name VARCHAR(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE,
    Category ENUM('wish','watch','watched'),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(Drama_Name) REFERENCES Drama_Table(Drama_Name)
) ENGINE=InnoDB;
"""
    )
    print("User_Table created successfully!")

    # Commit and close
    connection.commit()
    cursor.close()
    connection.close()


def drama_html_parser(link_of_drama):
    # initialization
    data = {}
    text = ""
    cast_list = []
    drama_page = requests.get(link_of_drama, headers=headers)
    souped = BeautifulSoup(drama_page.text, "lxml")

    # basic details
    for div in souped.find_all("div", class_="wpb_wrapper"):
        para = div.find("p")
        if para and "itle" in para.get_text():
            entries = para.get_text().split("\n")
            for entry in entries:
                data[entry.split(":", 1)[0].capitalize()] = entry.split(":", 1)[1]
            break

    # cast
    for em in souped.find_all("em"):
        if "Cast" in em.get_text():
            next_p = em.find_next_sibling("p")
            if next_p:
                # Split by <br/> tags
                for line in next_p.decode_contents().split("<br/>"):
                    line = BeautifulSoup(line, "lxml").get_text(strip=True)
                    if line:
                        cast_list.append(line)
    data["cast"] = cast_list

    # description
    text_column = souped.find_all("div", class_="wpb_wrapper")
    description = text_column[4].find_all("p")
    for part in description:
        text = text + (part.get_text(strip=True))
    data["description"] = text

    # some formatting hell
    years = re.findall(r"\d{4}", data["Broadcast period"])[0]
    data["Broadcast period"] = int(years)

    episodes = re.search(r"\d+", data["Episodes"])
    data["Episodes"] = int(episodes.group())

    if "Genres" in data.keys():
        data["Genre"] = data["Genres"]
        data.pop("Genres")

    if "Itle" in data.keys():
        data["Title"] = data["Itle"]
        data.pop("Itle")
    try:
        data.pop("Air time")
        data.pop("Broadcast network")
    except:
        pass

    # --- Data Entry ---
    query = """
INSERT IGNORE INTO Drama_Table (
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

    values = (
        data["Title"],
        int(data["Broadcast period"]),
        int(data["Episodes"]),
        data["description"],
        json.dumps(data["cast"], ensure_ascii=False),
        json.dumps(data["Genre"], ensure_ascii=False),
        None,
        None,
    )

    # Data Entry
    connection = mysql.connect(user="root", password="system", host="localhost")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()


os.system("cls" if os.name == 'nt' else 'clear')


def data_grabber():
    with open("data.html", "r") as file:
        content = file.read()
    soup = BeautifulSoup(content, "lxml")
    for section in soup.find_all("h2", class_="letter-title"):
        letter_wize_list = section.find_next_sibling("ul")
        if letter_wize_list:
            for anchors in letter_wize_list.find_all("li"):
                drama_tag = anchors.find("a")
                if drama_tag:
                    print(drama_tag.get_text())
                    drama_html_parser(drama_tag["href"])


def sql_to_csv():
    connection = mysql.connect(
        user="root", password="system", host="localhost", charset="utf8mb4"
    )
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    cursor.execute("SELECT * FROM drama_table;")
    list_of_all = cursor.fetchall()
    with open("dramas.csv", "a", newline="", encoding="utf-8") as file:
        writer_obj = csv.writer(file)
        for record in list_of_all:
            to_send = []
            for element in record:
                to_send.append(
                    element.encode("utf-8") if type(element) == "str" else element
                )
            writer_obj.writerow(to_send)


def csv_to_sql(path):
    connection = mysql.connect(user="root", password="system", host="localhost")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    query = """
INSERT IGNORE INTO Drama_Table (
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
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader_obj = csv.reader(file, quotechar='"', doublequote=True)
        for row in reader_obj:
            Drama_Name,Year,Episodes_Number,Description,Cast,Tags,Rating,Platform = row
            if Platform == '': Platform = json.dumps('None')
            row = (Drama_Name,Year,Episodes_Number,Description,Cast,Tags,Rating,Platform)
            cursor.execute(query, row)
            connection.commit()
    cursor.close()
    connection.close()

def ratings_to_sql():
    connection = mysql.connect(
        user="root", password="system", host="localhost", charset="utf8mb4"
    )
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    with open('other stuff/ratings.csv','r') as file:
        listed = []
        reader_obj = csv.reader(file)
        for record in reader_obj:
            name,rating = record[0],float(record[1])
            rating = round(rating*4,2)
            rating = round((math.log(rating + 1) / math.log(31)) * 9 + 1, 2)
            listed.append((name, rating))
    # Step 2: Sort ratings for percentile ranking
    sorted_ratings = sorted(r for _, r in listed)
    n = len(sorted_ratings)
    # Step 3: Assign percentile-based score and update DB
    for name, rating in listed:
        percentile = sorted_ratings.index(rating) / (n - 1)   # 0 → min, 1 → max
        new_rating = round(percentile * 9 + 1, 2)             # scale to 1–10
        print(name, rating)
        query = "UPDATE drama_table SET rating = %s WHERE drama_name LIKE %s;"
        cursor.execute(query, (new_rating, f"%{name}%"))
    connection.commit()
    cursor.close()
    connection.close()
