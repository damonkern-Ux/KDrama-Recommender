import mysql.connector as mysql
import re
import random
import unicodedata

# Genre grouping dictionary
GENRE_GROUPS = {
    "Drama": [
        "Melodrama",
        "Drama",
        "Life",
        "Family",
        "Youth",
        "School",
        "Period",
        "Historical",
        "Office",
        "Business",
        "Social",
        "Slice of Life",
    ],
    "Comedy": ["Comedy", "Sitcom", "Mockumentary", "Black comedy"],
    "Romance": ["Romance", "Romantic", "Bl", "Friendship"],
    "Action": [
        "Action",
        "Thriller",
        "Suspense",
        "Crime",
        "Detective",
        "Investigation",
        "Police",
        "Revenge",
        "Spy",
        "Military",
    ],
    "Fantasy": ["Fantasy", "Supernatural", "Horror"],
    "Mystery": ["Mystery", "Psychological"],
    "Science Fiction": [
        "Sci-fi",
        "Science fiction",
        "Science-fiction",
        "Time travel",
        "Time-travel",
    ],
    "Medical": ["Medical"],
    "Music & Arts": ["Music", "Musical"],
    "Sports": ["Sport", "Sports"],
    "Law & Politics": ["Law", "Legal", "Political", "Politic"],
    "Others": ["Other"],
}
connection = mysql.connect(host="localhost", user="root", password="system")
cursor = connection.cursor()
cursor.execute("USE dramas;")


def tags_getter(drama_seen):
    tag_list = []
    for drama in drama_seen:
        values = (f"%{drama}%",)
        cursor.execute(
            f"SELECT tags FROM drama_table WHERE drama_name LIKE %s;", values
        )
        rows = cursor.fetchall()
        if rows:
            tag_list.extend(rows[0][0].replace('"', "").split(","))
    final_tag_list = []
    for tag in tag_list:
        tag = tag.strip()
        for key, value in GENRE_GROUPS.items():
            if tag.capitalize() in value:
                final_tag_list.append(key)
    final_tag_list = list(set(final_tag_list))
    return final_tag_list


def tag_based_drama_getter(tag_list):
    drama_names = []
    for tag in tag_list:
        values = (f"%{tag.lower()}%",)
        cursor.execute(
            f"SELECT * FROM drama_table WHERE LOWER(tags) LIKE %s;",
            values,
        )
        for drama_name in cursor.fetchall():
            drama_names.append(drama_name)
    drama_names = list(set(drama_names))
    drama_final = []
    for drama in drama_names:
        drama_tag = [x.strip() for x in drama[5].replace('"', "").split(",")]
        intersection = list(set(tag_list) & set(drama_tag))
        if len(intersection) >= 3:
            drama_final.append(drama)
    return drama_final


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


def recommender():
    cursor.execute("SELECT drama_name FROM user_table;")
    dramas = []
    for name in cursor.fetchall():
        dramas.append(name[0])

    drama_list = tag_based_drama_getter(tags_getter(dramas))
    sorted_dramas = sorted(drama_list, key=lambda x: x[-2], reverse=True)
    drama_list = [normalize_title(x[0]) for x in sorted_dramas]
    dramas = [normalize_title(x) for x in dramas]
    final = [x for x in drama_list if x not in dramas]
    sampled = random.sample(final, 5)
    return_list = []
    for drama_name in sampled:
        values = (f"%{drama_name}%",)
        cursor.execute(
            f"SELECT drama_name,year,episodes_number,platform,description\
                FROM drama_table WHERE drama_name LIKE %s;",
            values,
        )
        return_list.append(cursor.fetchall()[0])
    return return_list


print(recommender()[0])
