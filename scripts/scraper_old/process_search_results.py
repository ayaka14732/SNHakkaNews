from bs4 import BeautifulSoup
import json
import re
from typing import Tuple

def strip_html(html_str: str) -> str:
    soup = BeautifulSoup(html_str, features='html.parser')
    return soup.get_text()

ignore_list = [
    '我市召开行风热线、城乡一线工作座谈会',
]

post_urls = set()

for i in range(1, 185 + 1):
    with open(f'search_results/{i}.json', encoding='utf-8') as f:
        o = json.load(f)

    assert o['errcode'] == 0

    news_items = o['data']['news']['list']

    for news_item in news_items:
        title = news_item['title']
        title = strip_html(title).strip()

        if '城乡一线' in title and title not in ignore_list:
            assert title.startswith('城乡一线')
            assert news_item['url'] == news_item['post_url']
            post_url = news_item['url']

            if post_url.endswith('.html'):
                post_urls.add(post_url)

def sort_criteria(post_url: str) -> Tuple[str, int]:
    url_prefix, post_id = re.fullmatch(r'(.+?)(\d+)\.html', post_url).groups()
    post_id = int(post_id)
    return url_prefix, post_id

assert len(set(post_url.rsplit('/', 1)[1] for post_url in post_urls)) == len(post_urls)

with open('post_urls.txt', 'w', encoding='utf-8') as f:
    for post_url in sorted(post_urls, key=sort_criteria):
        print(post_url, file=f)
