import requests
import mysql.connector as mysql
import json
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


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
        if para and re.search(r'\b\w*tle\b', para.get_text(), re.IGNORECASE):
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
    print(data)
    
    # some formatting hell
    years = re.findall(r"\d{4}", data["Broadcast period"])[0]
    data["Broadcast period"] = int(years)

    episodes = re.search(r"\d+",data["Episodes"])
    data["Episodes"] = int(episodes.group())
    
    if 'Genres' in data.keys():
        data['Genre'] = data['Genres']
        data.pop('Genres')
    if 'Itle' in data.keys():
        data['Title'] = data['Itle']
        data.pop('Itle')
    try:
        data.pop("Air time")
        data.pop("Broadcast network")
    except:pass
    return data


requirements = drama_html_parser("https://dramaday.me/my-dearest/")
