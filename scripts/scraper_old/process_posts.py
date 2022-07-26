import re
from typing import Optional, Tuple

broken_urls = [
    # no video date
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_764195.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_769587.html',
    # TODO: date wrong
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_769454.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_769453.html',
    # No video url
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_769144.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_769583.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_770603.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_785304.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_796693.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_797111.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_797519.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_798344.html',
    'http://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_801330.html',
]

def url_to_filename(url: str) -> str:
    return url.rsplit('/', 1)[1]

def get_video_date(page: str) -> Tuple[Optional[int], int, int]:
    match = re.search(r'<meta name="ArticleTitle" content="[ \t]*城乡一线（([^）"]+)[)）][ \t]*">', page)
    if not match:
        raise ValueError(f'Cannot handle post URL: {post_url}')

    date_str = match.group(1)
    match = re.fullmatch(r'((\d{4})年)?(\d{1,2})月(\d{1,2})日', date_str)
    year, month, day = match.group(2, 3, 4)

    year = int(year) if year else None
    month = int(month)
    day = int(day)

    return year, month, day

def get_publish_date(page: str) -> Tuple[int, int, int]:
    date_str = re.search(r'<span>发布时间：([^<]+)</span>', page).group(1)
    match = re.fullmatch('(\d{4})-(\d{2})-(\d{2})( \d{2}:\d{2}:\d{2})?', date_str)
    year, month, day = match.group(1, 2, 3)

    year = int(year)
    month = int(month)
    day = int(day)

    return year, month, day

def get_video_url(page: str) -> str:
    match = re.search(r'http.+?gdvideo\.southcn\.com.+?\.mp4', page)
    if match:
        return match.group(0).replace('\\', '')

    match = re.search(r'/xingning/files/(.+?).mp4', page)
    if match:
        return match.group(0)

    match = re.search(r'(/xingning/files/.+?)\n', page)
    if match:
        return match.group(1)

    raise ValueError(f'Cannot handle post URL: {post_url}')

with open('post_urls.txt', encoding='utf-8') as f:
    post_urls = [line.rstrip('\n') for line in f]

for post_url in post_urls:
    if post_url in broken_urls:
        continue

    with open('posts/' + url_to_filename(post_url), encoding='utf-8') as f:
        page = f.read()

    video_year, video_month, video_day = get_video_date(page)
    publish_year, publish_month, publish_day = get_publish_date(page)
    video_url = get_video_url(page)

    print(post_url, video_year, video_month, video_day, publish_year, publish_month, publish_day, video_url, sep=',')
