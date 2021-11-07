from datetime import date, datetime, timedelta

# https://stackoverflow.com/a/1060330
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def is_valid_url(url: str):
    return any(url.startswith(x) for x in ('http://', 'https://'))

def is_valid_key(k: str):
    return k.endswith('.mp4')

last_date = date(2015, 4, 16)

with open('list.csv') as f:
    next(f)  # skip header

    for i, line in enumerate(f, 1):
        date, post_url, video_url, video_key = line.rstrip('\n').split(',')

        if date == 'ORPHANED':
            continue

        date = datetime.strptime(date, '%Y%m%d').date()

        assert date == last_date + timedelta(1), f'Error on line {i}: Date must be continuous'
        assert post_url == 'ERROR' or is_valid_url(post_url), f'Error on line {i}'
        assert video_url == 'ERROR' or is_valid_url(video_url), f'Error on line {i}'
        assert video_key == 'ERROR' or is_valid_key(video_key), f'Error on line {i}'

        last_date = date
