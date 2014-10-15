import re

import requests
from bs4 import BeautifulSoup

CORIELL_BASE_URL = 'https://catalog.coriell.org/0/'
CORIELL_PIGI_URL = ('https://catalog.coriell.org/0/Sections/Collections/' +
                    'NIGMS/PGPs.aspx')
CORIELL_PIGI_URL_PARAMS = {'PgId': '772', 'coll': 'GM'}


def scrape():
    pigi_req = requests.get(CORIELL_PIGI_URL, params=CORIELL_PIGI_URL_PARAMS)

    if pigi_req.status_code == 200:
        soup = BeautifulSoup(pigi_req.text)
        pgp_table = soup.findAll(id='grdPgpPIGI')[0]
        urls = [x.get('href') for x in pgp_table.findAll('a')]
        for url in urls:
            if re.search(r'Sample_Detail', url):
                url = re.sub(r'^\.\./\.\./\.\./', CORIELL_BASE_URL, url)
                sample_req = requests.get(url)
                if not sample_req.status_code == 200:
                    print "URL not loading? " + url
                    continue
                sample_soup = BeautifulSoup(sample_req.text)
                remarks = sample_soup.findAll(id='lblCat_Remark')[0].get_text()
                if re.search(r'hu[0-9A-Fa-f]{6}', remarks):
                    huID = re.search(r'(hu[0-9A-Fa-f]{6})', remarks).groups()[0]
                    print huID
                else:
                    print "No huID found for URL: " + url

if __name__ == "__main__":
    scrape()
