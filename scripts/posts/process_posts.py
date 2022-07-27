import datetime
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
        raise ValueError('Cannot handle the page')

    date_str = match.group(1)
    match = re.fullmatch(r'((\d{4})年)?(\d{1,2})月(\d{1,2})日', date_str)
    year, month, day = match.group(2, 3, 4)

    year = int(year) if year else None
    month = int(month)
    day = int(day)

    return year, month, day

def get_publish_date(page: str) -> datetime.date:
    date_str = re.search(r'<span>发布时间：([^<]+)</span>', page).group(1)
    match = re.fullmatch('(\d{4})-(\d{2})-(\d{2})( \d{2}:\d{2}:\d{2})?', date_str)
    year, month, day = match.group(1, 2, 3)

    year = int(year)
    month = int(month)
    day = int(day)

    return datetime.date(year, month, day)

def get_video_url(page: str) -> str:
    match = re.search(r'http.+?gdvideo\.southcn\.com.+?\.mp4', page)
    if match:
        return match.group(0).replace('\\', '')

    match = re.search(r'/xingning/files/(.+?).mp4', page)
    if match:
        return 'http://www.xingning.gov.cn' + match.group(0)

    match = re.search(r'(/xingning/files/.+?)\n', page)
    if match:
        return 'http://www.xingning.gov.cn' + match.group(1)

    raise ValueError('Cannot handle the page')

def determine_real_date(video_date: Tuple[Optional[int], int, int], publish_date: datetime.date) -> datetime.date:
    threshold = datetime.timedelta(days=60)
    lower_range = publish_date - threshold
    upper_range = publish_date + threshold

    video_year, video_month, video_day = video_date

    for real_year in range(publish_date.year - 1, publish_date.year + 1 + 1):
        try:
            real_date = datetime.date(real_year, video_month, video_day)
        except ValueError:
            continue

        if lower_range < real_date < upper_range:
            if video_year is not None:
                assert real_year == video_year
            return real_date

    raise ValueError('Cannot determine real date')

with open('post_urls.txt', encoding='utf-8') as f:
    post_urls = [line.rstrip('\n') for line in f]

all_items = []

for post_url in post_urls:
    if post_url in broken_urls:
        continue

    with open('posts/' + url_to_filename(post_url), encoding='utf-8') as f:
        page = f.read()

    video_date = get_video_date(page)
    publish_date = get_publish_date(page)
    video_url = get_video_url(page)
    real_date = determine_real_date(video_date, publish_date)

    all_items.append((real_date, post_url, video_url))

for real_date, post_url, video_url in sorted(all_items):
    print(str(real_date), post_url, video_url, sep='\t')
