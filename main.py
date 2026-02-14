from  get_title   import create_requests, get_page, parse_html
from      ai      import get_summary 
from  send_email  import check_email, info, warn, err

from addon import check_zaobao, get_zaobao

if not check_email():
    raise Exception("Email configuration is incorrect or the SMTP server is unreachable. Please check your settings.")

sources = [
    ["www.wsj.com", ["us-news", "world", "business"]],
    ["www.wsj.com", ["politics", "economy"]],
    ["www.wsj.com", ["tech", "finance"]],
    ["www.reuters.com", []],
    ["www.bloomberg.com", ["news/articles"]],
    ["www.ft.com", ["content"]]
]
res = [parse_html(get_page(source)) for source in (create_requests(sources))]
if check_zaobao():
    sources.append([www.zaobao.com, []])
    res.append(get_zaobao())
if None in res:
    err("Error: Failed to retrieve data from one or more sources.")
    exit(1)
empty_indices = [index for index, element in enumerate(res) if element == []]
if len(empty_indices) > 0:
    warn(f"Empty value in {' and '.join([f'{sources[i][0]}/{child}' for i in empty_indices for child in sources[i][1]])}")
res = [item for sublist in res for item in sublist]  
if len(res) == 0:
    info("No news found.")
    exit(0)
res.sort(key=lambda x: ('hours' in x['date'], 'minutes' in x['date'], int(x['date'].split()[0])))
res = [item for item in res if (nums := item['date'].split()[:2]) and (not 'hours' in item['date'] or int(nums[0]) <= 9)]
try:
    info(get_summary(res))
except Exception as e:
    err(e.args[0])
    exit(1)
