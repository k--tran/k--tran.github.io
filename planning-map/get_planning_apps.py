#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import urllib
import time
import csv
from bs4 import BeautifulSoup
import csv, codecs, cStringIO

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
            
            url = "https://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx?sub={0}&page={1}".format(encoded_sub, page_num)
            req = requests.get(url, headers = {"User-Agent":"MMozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)"})
            soup = BeautifulSoup(req.content, 'lxml', from_encoding='Latin-1')
            tbl_rows = soup.find(attrs={"class": "permitsList"}).find_all('tr')
            print len(tbl_rows)
            for tbl_row in tbl_rows:
                #skip header row
                if tbl_row['class'] == ['heading1']:
                    cols = tbl_row.find_all('th')
                    addresses = list(cols[1].stripped_strings)
                elif tbl_row['class'] == ['heading2']:
                    pass
                elif tbl_row['class'] == ['detail']:
                    cols = tbl_row.find_all('td')
                    link = tbl_row.find_next('a').get('href')
                    description = cols[1].get_text().replace('\n', ' ').strip()
                    for address in addresses:
                        url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=AIzaSyBYDKuP2KKu93_LzHeh1UfDSQE_aF_8lOs".format(address)
                        req = requests.get(url).json()
                        lat = req['results'][0]['geometry']['location']['lat']
                        lng = req['results'][0]['geometry']['location']['lng']
                        list_of_apps.append((address, lat, lng, description, link))
                        print (address, lat, lng, description, link)

    except requests.ConnectionError:
        print "Connection error"
        pass
    print u'Done'
    
    return list_of_apps
    
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
    
def create_csv(data):
    
    with open('planning_apps.csv','w') as out:
        csv_out = UnicodeWriter(out)
        #csv_out=csv_writer.writer(out)
        csv_out.writerow(['Address', 'Lat', 'Long', 'Description', 'Link'])
        for row in data:
            csv_out.writerow(row)
            
http://stackoverflow.com/questions/28921096/loading-csv-with-filereader-to-make-js-objects-for-map-markers-maps-api
