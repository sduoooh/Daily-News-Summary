from  get_title   import create_requests, get_page, parse_html
from      ai      import get_summary 
from  send_email  import check_email, info, warn, err

from addon import check_zaobao, get_zaobao
from debug import debugger

def get_base_sources(sources):
    if not debugger.check_func_status("get_base_sources"):
        return [], []
    
    res = [parse_html(get_page(source)) for source in (create_requests(sources))]
    if None in res:
        err("Error: Failed to retrieve data from one or more sources.")
        exit(1)
    empty_indices = [index for index, element in enumerate(res) if element == []]
    warn_list = [f'{sources[i][0].split(".")[-2]}' for i in empty_indices] if len(empty_indices) > 0 else []
    return res, warn_list

def get_additional_sources():
    if not debugger.check_func_status("get_additional_sources"):
        return [], []
    zaobao = get_zaobao()
    warn_list = ["Lianhe Zaobao"] if len(zaobao) == 0 else []
    return zaobao, warn_list

def get_all_sources(sources):
    if not debugger.check_func_status("get_all_sources"):
        return []
    res, warn_list = get_base_sources(sources)
    if check_zaobao():
        zaobao, zaobao_warn_list = get_additional_sources()
        res.append(zaobao)
        warn_list.extend(zaobao_warn_list)
    if len(warn_list) > 0:
        warn(f"Empty value in {' and '.join(warn_list)}")
    res = [item for sublist in res for item in sublist]  
    if len(res) == 0:
        info("No news found.")
        exit(0)
    res.sort(key=lambda x: ('hours' in x['date'], 'minutes' in x['date'], int(x['date'].split()[0])))
    res = [item for item in res if (nums := item['date'].split()[:2]) and (not 'hours' in item['date'] or int(nums[0]) <= 9)]
    return res

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

try:
    res = get_all_sources(sources)
    summary = get_summary(res)
    info(summary)
except Exception as e:
    err(e.args[0])
    exit(1)
finally:
    debugger.print_debug_info()