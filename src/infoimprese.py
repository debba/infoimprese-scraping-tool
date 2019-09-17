import requests
from lxml import html
from src.decrypt import get_captcha, get_pec
from src.tree import get_contact_by_crawled_page, get_result_pages, count_from_search
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
    totResults = 0
    totPages = 1

    def set_query_params(self, dove, ricerca, page=None):
        self.queryParams['dove'] = dove
        self.queryParams['ricerca'] = ricerca
        if page is not None:
            self.queryParams['page'] = page

    def scrape_page(self, page):
        print("[OPEN PAGE] %d" % page)
        self.set_query_params(self.where, self.query, page)

        s = requests.session()
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
            'indiceFiglio': '3',
            'indice': self.queryParams['page'],
            'pagina': self.queryParams['page']-1
        })

        tree = html.fromstring(response.text)

        if page == 1:
            self.totResults, self.totPages = count_from_search(tree)
            print("[TOTAL RESULTS] %d" % self.totResults)
            print("[TOTAL PAGES] %d" % self.totPages)

        pages = get_result_pages(tree)
        for page in pages:
            crawled_page = s.get("%s/%s" % (API_ENDPOINT, page))
            contact = get_contact_by_crawled_page(crawled_page.text, self.scraperFields)
            print(contact)

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
        self.scrape_page(1)

        if self.totPages is not 1:
            for i in range(2, self.totPages):
                self.scrape_page(i)
