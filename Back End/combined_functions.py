import mysql.connector as mysql
import re
import json
import unicodedata
import PyMovieDb

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
    s = s.title()
    return s


def imdb_searcher(drama_name):
    buffer = PyMovieDb.IMDB()
    results = buffer.get_by_name(drama_name, tv=True)
    return results


def watched_list():
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    listed = []
    cursor.execute(
        "SELECT drama_name,timestamp FROM user_table WHERE LOWER(category)='watched';"
    )
    for drama in cursor.fetchall():
        time = str(drama[1])
        time = time.split()[0].split("-")[::-1]
        time = f"{time[0]}-{time[1]}-{time[2]}"
        values = (f"%{drama[0]}%",)
        cursor.execute(
            "SELECT drama_name,year,episodes_number FROM drama_table WHERE LOWER(drama_name) LIKE %s;",
            values,
        )
        elements = cursor.fetchall()[0]
        listed.append((elements[0], elements[1], elements[2], time))
    cursor.close()
    connection.close()
    return listed


def wish_list():
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    listed = []
    cursor.execute("SELECT drama_name FROM user_table WHERE LOWER(category)='wish';")
    for drama in cursor.fetchall():
        data = json.loads(imdb_searcher(normalize_title(drama[0])))
        time = data.get("datePublished").split("-")[0]
        info = (
            normalize_title(drama[0]),
            time,
            data.get("description"),
        )
        listed.append(info)
    cursor.close()
    connection.close()
    return listed


def watch_list():
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    listed = []
    cursor.execute("SELECT drama_name FROM user_table WHERE LOWER(category)='watch';")
    for drama in cursor.fetchall():
        data = json.loads(imdb_searcher(normalize_title(drama[0])))
        info = (
            normalize_title(drama[0]),
            data.get("datePublished").split("-")[0],
            data.get("description"),
        )
        listed.append(info)
    cursor.close()
    connection.close()
    return listed


def watch_listexplore():
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    listed = []
    cursor.execute("SELECT drama_name FROM user_table WHERE LOWER(category)='watch';")
    count = 0
    for drama in cursor.fetchall():
        data = json.loads(imdb_searcher(normalize_title(drama[0])))
        info = (
            normalize_title(drama[0]),
            data.get("datePublished").split("-")[0],
            data.get("description"),
        )
        listed.append(info)
        count = count + 1
        if count == 5:
            break
    cursor.close()
    connection.close()
    return listed


def profile():
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    cursor.execute("SELECT COUNT(drama_name) FROM user_table WHERE LOWER(category)='watch';")
    watch = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(drama_name) FROM user_table WHERE LOWER(category)='watched';")
    watched = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(drama_name) FROM user_table WHERE LOWER(category)='wish';")
    wish = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return [watch, watched, wish]


# def updater(drama_name, status):
#     try:
#         if status == "watched":
#             cursor.execute(
#                 "UPDATE user_table SET category='watched' WHERE drama_name LIKE %s;",
#                 (f"%{drama_name}%",),
#             )
#         elif status == "watch":
#             cursor.execute(
#                 "UPDATE user_table SET category='watch' WHERE drama_name LIKE %s;",
#                 (f"%{drama_name}%",),
#             )
#         elif status == "wish":
#             cursor.execute(
#                 "UPDATE user_table SET category='wish' WHERE drama_name LIKE %s;",
#                 (f"%{drama_name}%",),
#             )
#         elif status == "remove-wish":
#             cursor.execute(
#                 "DELETE FROM user_table WHERE drama_name LIKE %s;",
#                 (f"%{drama_name}%",),
#             )
#         elif status == "remove-watch":
#             cursor.execute(
#                 "DELETE FROM user_table WHERE drama_name LIKE %s;",
#                 (f"%{drama_name}%",),
#             )
#         return "done"
#     except Exception as e:
#         return e

