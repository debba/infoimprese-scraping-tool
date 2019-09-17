from src.utils import get_captcha, get_pec
import math
from src.infoimprese import Scraper, ScraperException
from lxml import html
import os

if __name__ == "__main__":

    '''
    url = 'http://www.infoimprese.it/impr/ricerca/popup_vetrina.jsp?ID=ltXigy7w0WgH&CHIAVE=ujoRqOQ1v6myCt93ZV0IZQ0%3D'
    api_key = 'ebee9ed945b9fa48cc6605694406b3c5'
    site_key = '6LefyWAUAAAAAA-MerRO-4rzv0C5RTS1CorjEwhl'  # grab from site

    pec = get_pec(url, api_key, site_key)
    print(pec)
    '''

    try:
        Scraper(query="ottica", where="milano", api_keys={
            "api_key": "ebee9ed945b9fa48cc6605694406b3c5",
            "site_key": "6LefyWAUAAAAAA-MerRO-4rzv0C5RTS1CorjEwhl"
        })
    except ScraperException as se:
        print("Error: " + str(se))
