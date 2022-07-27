import re
from typing import Tuple

def sort_criteria(post_url: str) -> Tuple[str, int]:
    url_prefix, post_id = re.fullmatch(r'(.+?)(\d+)\.html', post_url).groups()
    post_id = int(post_id)
    return url_prefix, post_id
    
post_urls = set()

with open('../search_results/post_urls.txt', encoding='utf-8') as f:
    for line in f:
        post_url = line.rstrip('\n')
        post_urls.add(post_url)

with open('../legacy/list.csv', encoding='utf-8') as f:
    next(f)  # skip header

    for line in f:
        _, post_url, _, _ = line.rstrip('\n').split(',')

        if post_url == 'ERROR':
            continue

        post_urls.add(post_url)

with open('post_urls.txt', 'w', encoding='utf-8') as f:
    for post_url in sorted(post_urls, key=sort_criteria):
        print(post_url, file=f)
