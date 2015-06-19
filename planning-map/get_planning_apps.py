#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

def planning_app_ids(suburb):
    
    list_of_apps = []
    encoded_sub = urllib.urlencode(suburb)

    try:
        url = "https://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx?sub={0}".format(encoded_sub)
        req = requests.get(url, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
        soup = BeautifulSoup(req.content, 'lxml', from_encoding='Latin-1')
        p_nums = soup.find(attrs={"class": "pageSummary"}).get_text(strip=True)
        total_p = re.search(urof\s(\d+)', p_nums).group(1) + 1)
        page_range = xrange(1, total_p/10 + 1)
        for page_num in page_range:
            url = "https://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx?sub={0}&page={1}".format(encoded_sub, page_num)
            req = requests.get(url, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
            soup = BeautifulSoup(req.content, 'lxml', from_encoding='Latin-1')
            tbl_rows = soup.find(attrs={"class": "permitsList"}).find_all('tr')
            for tbl_row in tbl_rows:
                #skip header row
                if re.search(u'Property Address', tbl_row) is not None:
                    continue
                elif tbl_row['class'] == 'heading1':
                    cols = tbl_row.find_all('th')
                    address = cols[1].get_text()
                elif tbl_row['class'] == 'heading2':
                    continue
                elif tbl_row['class'] == 'detail':
                    cols = tbl_row.find_all('td')
                    link = tbl_row.find_next('a').get('href')
                    description = col[1].get_text().replace('\n', ' ').strip()
                    list_of_apps.append(address, description, link)

    except requests.ConnectionError:
        print "Connection error"
        pass
    print u'Done'
    
    return list_of_apps
