from  get_title   import get_page, parse_html
from      ai      import get_summary 
from  send_email  import check_email, info, err

if not check_email():
    raise Exception("Email configuration is incorrect or the SMTP server is unreachable. Please check your settings.")

sources = ["www.reuters.com/world/china", "www.economist.com", "www.bloomberg.com/news/articles", "www.wsj.com", "www.scmp.com/news/china/article"]
res = [parse_html(get_page(source)) for source in sources]
if None in res:
    err("Error: Failed to retrieve data from one or more sources.")
    exit(1)
res = [item for sublist in res for item in sublist]  
if len(res) == 0:
    info("No new articles found.")
    exit(0)
print(len(res))
res.sort(key=lambda x: (int(x['date'].split()[0]), 'minutes' in x['date'], 'hours' in x['date']))
try:
    info(get_summary(res))
except Exception as e:
    err(str(e))
    exit(1)
