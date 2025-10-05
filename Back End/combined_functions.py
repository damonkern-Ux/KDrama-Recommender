import mysql.connector as mysql
import re
import json
import unicodedata
import PyMovieDb

connection = mysql.connect(host="localhost", user="root", password="system")
cursor = connection.cursor()
cursor.execute("USE dramas;")


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


def imdb_searcher(drama_name):
    buffer = PyMovieDb.IMDB()
    results = buffer.get_by_name(drama_name, tv=True)
    return results


def watched_list():
    listed = []
    cursor.execute("SELECT drama_name FROM user_table WHERE LOWER(category)='watched'")
    for drama in cursor.fetchall():
        values = (f"%{drama[0]}%",)
        cursor.execute(
            "SELECT drama_name,year,episodes_number FROM drama_table WHERE LOWER(drama_name) LIKE %s",
            values
        )
        elements = cursor.fetchall()[0]
        listed.append((normalize_title(elements[0]), elements[1], elements[2]))
    return listed


def wish_list():
    listed = []
    cursor.execute("SELECT drama_name FROM user_table WHERE LOWER(category)='wish'")
    for drama in cursor.fetchall():
        data = json.loads(imdb_searcher(normalize_title(drama[0])))
        info = (normalize_title(drama[0]),data.get("datePublished"),data.get("description"))
        listed.append(info)
    return listed


def watch_list():
    listed = []
    cursor.execute("SELECT drama_name FROM user_table WHERE LOWER(category)='watch'")
    for drama in cursor.fetchall():
        data = json.loads(imdb_searcher(normalize_title(drama[0])))
        info = (normalize_title(drama[0]),data.get("datePublished"),data.get("description"))
        listed.append(info)
    return listed

