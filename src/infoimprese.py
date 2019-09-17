import requests
from lxml import html
from src.decrypt import get_captcha, get_pec
from src.tree import get_contact_by_crawled_page
import math

API_ENDPOINT = "https://www.infoimprese.it/impr"


class ScraperException(Exception):
    pass


class Scraper:
    apiKeys = None
    scraperFields = [
        "Denominazione",
        "Sede legale",
        "Attività",
        "Sede operativa",
        "Indirizzo web",
        "Posta elettronica",
        "Commercio elettronico",
        "Chi siamo",
        "Cosa facciamo",
        "Classe di fatturato",
        "Canali di vendita",
        "Marchi",
        "Principali paesi di export",
        "Certificazioni"
    ]
    queryParams = {
        "cer": 1,
        "pagina": 0,
        "flagDove": 'true',
        "dove": "",
        "ricerca": "",
        "g-recaptcha-response": ""
    }

    def set_query_params(self, dove, ricerca, page=None):
        self.queryParams['dove'] = dove
        self.queryParams['ricerca'] = ricerca
        if page is not None:
            self.queryParams['page'] = page

    def get_pages(self, text):

        tree = html.fromstring(text)
        tot_results = int(tree.xpath(
            '//html/body/center/table[2]/tr[2]/td[1]/table[1]/tr/td/table[2]/tr/td[1]/font/text()[2]')[0].lstrip(
            ' \xa0 n° '))
        tot_pages = math.ceil(tot_results / 10)

        pages = []

        for i in range(3, 13):
            xpath = "/html/body/center/table[2]/tr[2]/td[1]/table[1]/tr/td/table[%d]/tr[2]/td/table/tr/td[2]/a[" \
                    "1]/@onclick" % i

            try:
                pages.append("%s/ricerca/%s" % (API_ENDPOINT, tree.xpath(xpath)[0][14:-33]))
            except IndexError as e:
                print("ERR: %s" % str(e))

        return pages

    def update_page(self):
        self.queryParams["pagina"] += 1

    def __init__(self, query=None, where=None, config=None):
        if query is None:
            raise ScraperException("Query clause is undefined")
        if where is None:
            raise ScraperException("Where clause is undefined")

        if config is not None:
            self.apiKeys = config['anticaptcha']
            if config['scraper'] is not None and config['scraper']['fields'] is not None:
                self.scraperFields = config['scraper']['fields']

        self.query = query
        self.where = where
        self.set_query_params(self.where, self.query, 1)

        s = requests.session()

        s.get(API_ENDPOINT + "/index.jsp", headers={
            'Referer': 'https://www.infoimprese.it/impr/ricerca/risultati_globale.jsp',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/77.0.3865.75 Safari/537.36 '
        })

        url = API_ENDPOINT + "/ricerca/lista_globale.jsp"

        self.queryParams['g-recaptcha-response'] = get_captcha(
            url,
            self.apiKeys['api_key'],
            self.apiKeys['site_key']
        )

        if self.queryParams['g-recaptcha-response'] is None:
            raise ScraperException("Recaptcha checking failed.")

        s.post(url, data=self.queryParams)

        url = API_ENDPOINT + "/ricerca/risultati_globale.jsp"

        response = s.post(url, data={
            'cer': 1,
            'statistiche': 'S',
            'tipoRicerca': '1',
            'indiceFiglio': '3'
        })

        pages = self.get_pages(response.text)
        for page in pages:
            crawled_page = s.get(page)
            contact = get_contact_by_crawled_page(crawled_page.text, self.scraperFields)
            print(contact)
