
from bs4 import BeautifulSoup
import re
import requests
from typing import Tuple

def title2date(title: str) -> Tuple[int, int]:
    date_str = re.fullmatch(r'城乡一线（(.+)）', title).group(1)
    month, day = re.fullmatch(r'(\d{1,2})月(\d{1,2})日', date_str).group(1, 2)
    return month, day

response = requests.get('http://www.xingning.gov.cn/jrxn/spxw/cxyx/')
response.raise_for_status()
html_str = response.text

soup = BeautifulSoup(html_str, features='html.parser')

for li in soup.select('.g_main .list_right .listpicture_box ul li'):
    title = li.select_one('p').get_text()
    post_url = li.select_one('a')['href']
    month, day = title2date(title)
    print(month, day, post_url)
