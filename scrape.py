from bs4 import BeautifulSoup
import datetime
import re
import requests
from typing import Tuple

def get_last_date() -> datetime.date:
    with open('list.csv', encoding='utf-8') as f:
        for line in f:
            pass  # locate the last line
        video_date, _, _, _ = line.rstrip('\n').split(',')
        return datetime.date.fromisoformat(video_date)

def download_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def title2date(title: str) -> Tuple[int, int]:
    date_str = re.fullmatch(r'城乡一线（(.+)）', title).group(1)
    month, day = re.fullmatch(r'(\d{1,2})月(\d{1,2})日', date_str).group(1, 2)

    month = int(month)
    day = int(day)

    return month, day

def determine_video_date(month: int, day: int) -> datetime.date:
    today = datetime.date.today()
    threshold = datetime.timedelta(days=60)
    lower_range = today - threshold
    upper_range = today + threshold

    for year in range(today.year - 1, today.year + 1 + 1):
        try:
            video_date = datetime.date(year, month, day)
        except ValueError:
            continue

        if lower_range < video_date < upper_range:
            return video_date

    raise ValueError('Cannot determine real date')

def get_video_url(page: str) -> str:
    match = re.search(r'http.+?gdvideo\.southcn\.com.+?\.mp4', page)
    if match:
        return match.group(0).replace('\\', '')
    raise ValueError('Cannot handle the page')

if __name__ == '__main__':
    last_video_date = get_last_date()

    html_str = download_url('http://www.xingning.gov.cn/jrxn/spxw/cxyx/index.html')

    new_posts = []

    for li in BeautifulSoup(html_str, features='html.parser').select('.g_main .list_right .listpicture_box ul li'):
        title = li.select_one('p').get_text().replace(' ', '')
        post_url = li.select_one('a')['href']
        month, day = title2date(title)
        video_date = determine_video_date(month, day)

        if video_date <= last_video_date:
            break

        page = download_url(post_url)
        video_url = get_video_url(page)

        new_posts.append((video_date, post_url, video_url))

    for video_date, post_url, video_url in reversed(new_posts):
        print(video_date, post_url, video_url, sep='\t')
