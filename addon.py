import time
import json
from requests import get
from bs4 import BeautifulSoup

from config import ZAOBAO_SHADOW
from debug import RuntimeValue, debugger

def date_transfer(date_string):
    now = int(time.time())
    diff = now - int(date_string)
    if diff < 60:
        return f"{diff} seconds ago"
    elif diff < 3600:
        return f"{diff // 60} minutes ago"
    else:
        return f"{diff // 3600} hours ago"

def check_zaobao():
    if not debugger.check_func_status("check_zaobao"):
        return True
    return bool(ZAOBAO_SHADOW)

def raw2json(raw, debugs):
    l1 = BeautifulSoup(raw, 'html.parser').find_all('script')
    l1.sort(key=lambda x: len(x.text), reverse=True)
    l2 = l1[0].text
    debugs(l2)
    start_pos = l2.index("{")
    last_pos = l2.rindex("}") + 1
    l2 = '[' + l2[start_pos:last_pos].replace('\\"', '"') + ']'
    l2 = json.loads(l2)
    start_pos = l2.index("id")
    end_pos = l2.index("tagName")
    l3: list = l2[start_pos:end_pos]
    res = []
    res.append({"publisher": "Lianhe Zaobao", "title": l3[3], "date": l3[5]})
    t = []
    first = True
    for i in l3:
        if first:
            if type(i) != dict:
                continue
            else:
                first = False
                continue
        if type(i) != dict:
            t.append(i)
        else:
            res.append({"publisher": "Lianhe Zaobao", "title": t[1], "date": t[2]})
            t = []
    res.append({"publisher": "Lianhe Zaobao", "title": t[1], "date": t[2]})
    debugger.add_debug_info("addon", "raw2json", "reslist", [RuntimeValue("res", res)])
    return res

def get_zaobao(debugs):
    response = get(ZAOBAO_SHADOW)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        return None
    try:
        article_json = raw2json(response.text, debugs)
        return [{"publisher": "Lianhe Zaobao", "title": article["title"], "date": date_transfer(article["date"])} for article in article_json]
    except Exception as e:
        raise e
        

