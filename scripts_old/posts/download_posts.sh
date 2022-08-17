#!/bin/sh
aria2c -c --auto-file-renaming=false -i post_urls.txt -j1024 -d posts
