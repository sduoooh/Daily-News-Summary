import time
import json
from requests import get
from bs4 import BeautifulSoup

from config import ZAOBAO_SHADOW

def date_transfer(date_string):
    now = int(time.time())
    diff = now - int(date_string)
    if diff < 60:
        return f"{diff} seconds ago"
    elif diff < 3600:
        return f"{diff // 60} minutes ago"
    else:
        return f"{diff // 3600} hours ago"

def get_zaobao():
    response = get(ZAOBAO_SHADOW)
    response.encoding = 'utf-8' 
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    article_json = json.loads(json.loads(soup.find_all('script')[-1].text[48:-2]))["loaderData"]['0-0']["context"]["payload"]["articles"]
    return [{"publisher": "Lianhe Zaobao", "title": article["title"], "date": date_transfer(article["timestamp"])} for article in article_json]