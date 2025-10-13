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
        description = data.get("description")
        if description is None:
            description = "Description Not Available."
        try:
            time = data.get("datePublished").split("-")[0]
        except:
            time = "Time Not Available."
        info = (
            normalize_title(drama[0]),
            time,
            description,
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
        values = (f"%{drama[0]}%",)
        cursor.execute(
            "SELECT drama_name,year,episodes_number,description FROM drama_table WHERE LOWER(drama_name) LIKE %s;",
            values,
        )
        data = cursor.fetchall()[0]
        if data:
            listed.append([data[0], data[1], data[2], data[3]])
        else:
            listed.append([drama[0], "Not Available", "Not Available", "Not Available"])
    cursor.close()
    connection.close()
    return listed


def watch_listexplore():
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    listed = []
    count = 0
    cursor.execute("SELECT drama_name FROM user_table WHERE LOWER(category)='watch';")
    for drama in cursor.fetchall():
        values = (f"%{drama[0]}%",)
        cursor.execute(
            "SELECT drama_name,year,episodes_number,description FROM drama_table WHERE LOWER(drama_name) LIKE %s;",
            values,
        )
        data = cursor.fetchall()[0]
        count += 1
        if data:
            listed.append([data[0], data[1], data[2], data[3]])
        else:
            listed.append([drama[0], "Not Available", "Not Available", "Not Available"])
        if count == 5:
            break
    cursor.close()
    connection.close()
    return listed


def profile():
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    cursor.execute(
        "SELECT COUNT(drama_name) FROM user_table WHERE LOWER(category)='watch';"
    )
    watch = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(drama_name) FROM user_table WHERE LOWER(category)='watched';"
    )
    watched = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(drama_name) FROM user_table WHERE LOWER(category)='wish';"
    )
    wish = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return [watch, watched, wish]


def database_updator(drama_name, action):
    if drama_name.lower() == "search something":
        return "Nothing"
    drama_name = normalize_title(drama_name)
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    cursor.execute(
        "SELECT drama_name, category FROM user_table WHERE LOWER(drama_name) LIKE %s;",
        (f"%{drama_name.lower()}%",),
    )
    data = cursor.fetchall()
    actions_dictionary = {
        "add to watchlist": 101,
        "mark as watched": 102,
        "mark as wish": 103,
        "remove from watchlist": 201,
        "remove from wishlist": 301,
    }
    action_id = actions_dictionary[action.lower()]
    if data:
        if action_id == 101:
            cursor.execute(
                "UPDATE user_table SET category = 'watch' WHERE LOWER(drama_name) LIKE %s;",
                (f"%{drama_name.lower()}%",),
            )
        elif action_id == 102:
            cursor.execute(
                "UPDATE user_table SET category = 'watched' WHERE LOWER(drama_name) LIKE %s;",
                (f"%{drama_name.lower()}%",),
            )
        elif action_id == 103:
            cursor.execute(
                "UPDATE user_table SET category = 'wish' WHERE LOWER(drama_name) LIKE %s;",
                (f"%{drama_name.lower()}%",),
            )
        elif action_id == 201:
            cursor.execute(
                "DELETE FROM user_table WHERE LOWER(drama_name) LIKE %s;",
                (f"%{drama_name.lower()}%",),
            )
        elif action_id == 301:
            cursor.execute(
                "DELETE FROM user_table WHERE LOWER(drama_name) LIKE %s;",
                (f"%{drama_name.lower()}%",),
            )

    else:
        if action_id == 101:
            cursor.execute(
                "INSERT INTO user_table(drama_name, category) VALUES(%s,'watch');",
                (f"{drama_name.lower()}",),
            )
        elif action_id == 102:
            cursor.execute(
                "INSERT INTO user_table(drama_name, category) VALUES(%s,'watched');",
                (f"{drama_name.lower()}",),
            )
        elif action_id == 103:
            cursor.execute(
                "INSERT INTO user_table(drama_name, category) VALUES(%s,'wish');",
                (f"{drama_name.lower()}",),
            )
    connection.commit()
    cursor.close()
    connection.close()


def search(drama_name):
    drama_name = normalize_title(drama_name).lower()
    connection = mysql.connect(host="localhost", user="root", password="system")
    cursor = connection.cursor()
    cursor.execute("USE dramas;")
    cursor.execute(
        "SELECT * FROM drama_table WHERE LOWER(drama_name) LIKE %s;",
        (f"%{drama_name}%",),
    )
    listed = []
    for drama in cursor.fetchall():
        name = drama[0]
        year = drama[1]
        episodes = drama[2]
        description = drama[3]
        platform = drama[7]
        listed.append([name, year, episodes, platform, description])
    cursor.close()
    connection.close()
    return listed
