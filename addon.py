import time
from requests import get
from bs4 import BeautifulSoup

def date_transfer(date_string):
    if ":" in date_string:
        date_h, date_m = map(int, date_string.split(":"))
        now_h, now_m = time.localtime().tm_hour, time.localtime().tm_min
        diff_m = (now_h - date_h) * 60 + (now_m - date_m)
        return f"{diff_m // 60} hours ago"
    else:
        return date_string.replace("分钟前", " minutes ago")

def get_zaobao():
    url = f"https://www.zaobao.com/realtime/china"
    response = get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    response.encoding = 'utf-8' 
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    return [{"publisher": "Lianhe Zaobao", "title": article.find("a").get("title"), "date": date_transfer(article.find("span").text)} for article in soup.find_all('article')]