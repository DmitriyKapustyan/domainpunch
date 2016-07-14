#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, requests, time, string, json
import csv
import codecs

from io import StringIO

BASE_DIR = "D:\\"
LOG_FILE = 'domain.csv'
MAX_LIMIT_RESPONSE_COUNT = 50000

request_headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding":"gzip, deflate, sdch, br","Accept-Language":"ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4", "Host":"domainpunch.com"}

response = requests.get('https://domainpunch.com/tlds/daily.php?tlds&draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=2&order%5B0%5D%5Bdir%5D=desc&start=0&length=1500&search%5Bvalue%5D=&search%5Bregex%5D=false&_=' + str(time.time()), headers=request_headers)
ids = []
f = open(BASE_DIR + LOG_FILE, 'w')
writer = csv.writer(f, delimiter=';', lineterminator='\n')
writer.writerow(('zone', 'domain'))
if response.status_code  == requests.codes.ok:
    ids_raw = response.json()['data']
    for id_raw in ids_raw:
        id = id_raw['DT_RowId'].replace('_', '=')
        count_responses = []
        request_count = int(id_raw['3'])
        while request_count - MAX_LIMIT_RESPONSE_COUNT > 0:
            count_responses.append(MAX_LIMIT_RESPONSE_COUNT)
            request_count -= MAX_LIMIT_RESPONSE_COUNT
        count_responses.append(request_count)
        for count_response in count_responses:
            print(count_response)
            response = requests.get('https://domainpunch.com/tlds/daily.php?domains&draw=3&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=false&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=false&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=2&order%5B0%5D%5Bdir%5D=asc&start=0&length=' + str(count_response) + '&search%5Bvalue%5D=&search%5Bregex%5D=false&' + id + '&_=' + str(time.time()), headers=request_headers)
            if response.status_code  == requests.codes.ok:
                domains_raw = response.json()['data']
                for domain in domains_raw:
                    if isinstance(domain['1'], str):
                        domain['1'] = str(domain['1'])
                    if isinstance(id_raw['1'], str):
                        id_raw['1'] = str(id_raw['1'])                             
                    writer.writerow((id_raw['1'].encode("utf-8"), domain['1'].encode("utf-8")))                                
    f.close()
else:
    print(response.status_code)
