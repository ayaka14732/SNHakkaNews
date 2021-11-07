# Video list of daily news broadcast in Shin Neng Hakka

## Motivation

Shin Neng Hakka (兴宁客家话) is a (sub-)dialect of Hakka spoken in the Xingning City (兴宁市). The daily news section broadcast by 兴宁市广播电视台 (Xingning Radio and Television Station), which is called 城乡一线 (urban and rural on one line), is a high-quality resource of Shin Neng Hakka. The daily news is about 10 minutes in length, and the host’s voice is clear. This repository provides a list of all the videos and their permanent links from April 17, 2015 to the present.

## Data format

Currently the sanitized list, `list-sanitized.csv`, contains 881 entries of videos. This is less than one may expect because the video was not posted on some days or the link expires. On the other hand, the full list, `list.csv`, contains all the entries, including the missing and the expired ones. In most cases, you may not wish to use the full list.

The data is in CSV format, which consists of 4 columns:

- `DATE`: The date of the news
- `POST_URL`: The URL of the original webpage of the news
- `VIDEO_URL`: The URL of the video, extracted from the original webpage
- `VIDEO_KEY`: The key of the video file (for backup purpose, see below)

## Backup of the videos

To prevent more videos from becoming inaccessible due to expiry, videos that are currently accessible are backed up to Google Cloud Storage. You can access each video by its `VIDEO_KEY`.

- gsutil URI: `gs://fantastisk-klynge/{VIDEO_KEY}`
- HTTPS link: `https://storage.googleapis.com/fantastisk-klynge/{VIDEO_KEY}`

Example: If the `VIDEO_KEY` is `20150417ACEGIK.mp4`, then

- the gsutil URI would be `gs://fantastisk-klynge/20150417ACEGIK.mp4`
- the HTTPS link would be `https://storage.googleapis.com/fantastisk-klynge/20150417ACEGIK.mp4`

## Update

The full list is manually updated.

Check the data integrity of the list after each update:

```sh
python check.py
```

Generate a new sanitized list:

```sh
grep -v ERROR list.csv > list-sanitized.csv
```
