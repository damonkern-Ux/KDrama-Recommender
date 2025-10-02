import requests
from bs4 import BeautifulSoup
import re
def trending():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/140.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get("https://www.imdb.com/search/title/?genres=drama&countries=KR",headers=HEADERS)
    except:
        return []
    soup = BeautifulSoup(response.text,"html.parser")
    dramas = []
    count=0
    for item in soup.find_all('li',class_='ipc-metadata-list-summary-item'):
        text = item.get_text()
        match = re.match(r"^\d+\.\s*(.+?)(?=\d{4})", text)
        if match:
            drama_name = match.group(1).strip()
            dramas.append(drama_name)
        count+=1
        if count%15==0:break
    return dramas