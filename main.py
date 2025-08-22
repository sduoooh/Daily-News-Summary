from  get_title   import create_requests, get_page, parse_html
from      ai      import get_summary 
from  send_email  import check_email, info, err

import time

if not check_email():
    raise Exception("Email configuration is incorrect or the SMTP server is unreachable. Please check your settings.")

sources = [
    ["www.wsj.com", ["us-news", "world", "business", "politics", "economy", "tech", "finance"]],
    ["www.reuters.com", []],
    ["www.economist.com", []],
    ["www.bloomberg.com", []],
    ["www.ft.com", []]
]
time_str = f"after%3A{time.strftime('%Y-%m-%d', time.gmtime(time.time() - 86400))}%20before%3A{time.strftime('%Y-%m-%d', time.gmtime(time.time() + 86400))}"
res = [parse_html(get_page(time_str, source)) for source in (create_requests(sources))]
if None in res:
    err("Error: Failed to retrieve data from one or more sources.")
    exit(1)
res = [item for sublist in res for item in sublist]  
if len(res) == 0:
    info("No new articles found.")
    exit(0)
res.sort(key=lambda x: ('hours' in x['date'], 'minutes' in x['date'], int(x['date'].split()[0])))

try:
    info(get_summary(res))
except Exception as e:
    err(str(e))
    exit(1)
