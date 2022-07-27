#!/bin/sh
aria2c -c -i post_urls.txt -j128 -d posts
