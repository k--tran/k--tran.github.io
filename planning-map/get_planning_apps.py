#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import urllib
import time
from bs4 import BeautifulSoup

def planning_app_ids(suburb):
    
    list_of_apps = []
    encoded_sub = urllib.quote(suburb)

    try:
        url = "https://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx?sub={0}".format(encoded_sub)
        req = requests.get(url, headers = {"User-Agent":"Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)"})
        soup = BeautifulSoup(req.content, 'lxml', from_encoding='Latin-1')
        p_nums = soup.find(attrs={"class": "pageSummary"}).get_text(strip=True)
        total_p = int(re.search(ur'of\s(\d+)', p_nums).group(1)) + 1
        page_range = xrange(1, total_p/10 + 1)
        for page_num in page_range:
            print page_num
            time.sleep(1)
            url = "https://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx?sub={0}&page={1}".format(encoded_sub, page_num)
            req = requests.get(url, headers = {"User-Agent":"MMozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)"})
            soup = BeautifulSoup(req.content, 'lxml', from_encoding='Latin-1')
            tbl_rows = soup.find(attrs={"class": "permitsList"}).find_all('tr')
            print len(tbl_rows)
            for tbl_row in tbl_rows:
                #skip header row
                if tbl_row['class'] == ['heading1']:
                    cols = tbl_row.find_all('th')
                    address = cols[1].get_text()
                elif tbl_row['class'] == ['heading2']:
                    pass
                elif tbl_row['class'] == ['detail']:
                    cols = tbl_row.find_all('td')
                    link = tbl_row.find_next('a').get('href')
                    description = cols[1].get_text().replace('\n', ' ').strip()
                    list_of_apps.append((address, description, link))
                    print address

    except requests.ConnectionError:
        print "Connection error"
        pass
    print u'Done'
    
    return list_of_apps
