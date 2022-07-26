#!/bin/sh
mkdir -p search_results
for i in {1..185}; do
  if [ ! -f search_results/$i.json ]; then
    curl 'http://search.gd.gov.cn/api/search/all' \
      -H 'Accept: application/json, text/plain, */*' \
      -H 'Accept-Language: en-US,en;q=0.5' \
      -H 'Content-Type: application/json' \
      -H 'Cookie: cmssearch_session=UL7UAV16s70P4Rd5jDorshUikEcfLaAc7qRe4pY8; SEARCH_LIST=%5B%22%5Cu57ce%5Cu4e61%5Cu4e00%5Cu7ebf%22%5D; XSRF-TOKEN=eyJpdiI6IkVUR012clFFbjY2NWRTVklDM3p3alE9PSIsInZhbHVlIjoiXC9RdzF0SGFlY09BdnlZV0c5KzFuVWYzMk1pdEtsSmIrQUZCYnFaUkN6QmRCQUpiTWJFODNxN2ExVzc5ODA4RjYiLCJtYWMiOiIzYTUzNjFmMTgyMzhkOTk5ODkyZmNkMThlOThjZWU4ZDQyNjY0NmU1NGIxMDMxYzVjOTZlYjZiZTg2ZDRmNjU3In0%3D' \
      -H 'Origin: http://search.gd.gov.cn' \
      -H 'Proxy-Connection: keep-alive' \
      -H "Referer: http://search.gd.gov.cn/search/all/753004?page=$i&keywords=%E5%9F%8E%E4%B9%A1%E4%B8%80%E7%BA%BF&filterType=localSite&filterId=undefined" \
      -H 'Sec-GPC: 1' \
      -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36' \
      -H 'X-XSRF-TOKEN: eyJpdiI6IkVUR012clFFbjY2NWRTVklDM3p3alE9PSIsInZhbHVlIjoiXC9RdzF0SGFlY09BdnlZV0c5KzFuVWYzMk1pdEtsSmIrQUZCYnFaUkN6QmRCQUpiTWJFODNxN2ExVzc5ODA4RjYiLCJtYWMiOiIzYTUzNjFmMTgyMzhkOTk5ODkyZmNkMThlOThjZWU4ZDQyNjY0NmU1NGIxMDMxYzVjOTZlYjZiZTg2ZDRmNjU3In0=' \
      --data-raw '{"page":"'$i'","keywords":"城乡一线","sort":"smart","site_id":"753004","range":"site","position":"title","recommand":1,"gdbsDivision":"441481","service_area":753}' \
      --compressed \
      --insecure \
      -o search_results/$i.json &
  fi
done
wait
