from requests import get
from bs4 import BeautifulSoup
from urllib.request import quote

def create_requests(sources):
    return map(lambda x: quote(" OR ".join([f"site:{x[0]}/" + target for target in x[1]])).replace("/", "%2F") if len(x[1]) > 0 else f"site:{x[0]}", sources)

def get_page(time_key, source):
    source = f"{time_key}%20({source})"
    url = f"https://news.google.com/search?q={source}&hl=en-US&gl=US&ceid=US%3Aen"
    response = get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
    if response.status_code != 200:
        return None
    return response.text

def parse_html(html):
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    item_a = soup.find_all('a', class_='JtKRv')
    items = []

    for a in item_a:
        partial = a.get('aria-label', '').split(' - ')
        date = partial[-1]
        if "minutes ago" in date or "hours ago" in date:
            pb_index = -2
        elif "minutes ago" in partial[-2] or "hours ago" in partial[-2]:
            date = partial[-2]
            pb_index = -3
        else:
            continue
            
        title = a.get_text(strip=True)
        publisher = partial[pb_index]
        items.append({'publisher': publisher, 'title': title, 'date': date})

    return items