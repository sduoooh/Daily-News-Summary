import time
from requests import get
from bs4 import BeautifulSoup

from config import ZAOBAO_SHADOW

def date_transfer(date_string):
    if ":" in date_string:
        date_h, date_m = map(int, date_string.split(":"))
        now_h, now_m = time.localtime().tm_hour, time.localtime().tm_min
        diff_m = (now_h - date_h) * 60 + (now_m - date_m)
        return f"{diff_m // 60} hours ago"
    else:
        return date_string.replace("分钟前", " minutes ago")

def get_zaobao():
    response = get(ZAOBAO_SHADOW)
    response.encoding = 'utf-8' 
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Fetched {len(soup.find_all('article'))} articles from Lianhe Zaobao")
    return [{"publisher": "Lianhe Zaobao", "title": article.find("a").get("title"), "date": date_transfer(article.find("span").text)} for article in soup.find_all('article')]

print(get_zaobao())