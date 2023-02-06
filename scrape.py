from bs4 import BeautifulSoup
import datetime
import re
import requests
import sys

def determine_date(title: str) -> str:
    date_str = re.fullmatch(r'城乡一线（(.+)）', title).group(1)
    month, day = re.fullmatch(r'(\d{1,2})月(\d{1,2})日', date_str).group(1, 2)

    month = int(month)
    day = int(day)

    today = datetime.date.today()
    threshold = datetime.timedelta(days=60)
    lower_range = today - threshold
    upper_range = today + threshold

    for year in range(today.year - 1, today.year + 1 + 1):
        try:
            date = datetime.date(year, month, day)
        except ValueError:
            continue

        if lower_range < date < upper_range:
            return date.strftime('%Y-%m-%d')

    raise ValueError('Cannot determine real date')

def download_url(url: str) -> str:
    sys.stderr.write(f'Requesting {url}\n')
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_video_url(page: str) -> str:
    match = re.search(r'http.+?gdvideo\.southcn\.com.+?\.mp4', page)
    if match:
        return match.group(0).replace('\\', '')
    raise ValueError('Cannot handle the page')

def get_post_id(post_url: str) -> int:
    match = re.search(r'https?://www.xingning.gov.cn/jrxn/spxw/cxyx/content/post_(\d+).html', post_url)
    if match:
        return int(match.group(1))
    raise ValueError('Cannot handle the post URL')

if __name__ == '__main__':
    data = {}

    with open('list.csv', encoding='utf-8') as f:
        for line in f:
            date, post_id, post_url, video_url = line.rstrip('\n').split(',')
            post_id = int(post_id)
            data[date] = post_id, post_url, video_url

    html_str = download_url('https://www.xingning.gov.cn/jrxn/spxw/cxyx/index.html')
    soup = BeautifulSoup(html_str, features='html.parser')
    video_items = soup.select('.g_main .list_right .listpicture_box ul li')

    for li in video_items:
        post_url = li.select_one('a')['href']
        post_id = get_post_id(post_url)
        title = li.select_one('p').get_text().replace(' ', '')
        date = determine_date(title)
        page = download_url(post_url)
        video_url = get_video_url(page)
        data[date] = post_id, post_url, video_url

    with open('list.csv', 'w', encoding='utf-8') as f:
        for date, (post_id, post_url, video_url) in sorted(data.items()):
            print(date, post_id, post_url, video_url, sep=',')
