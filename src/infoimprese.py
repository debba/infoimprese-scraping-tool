import requests
from lxml import html
from src.decrypt import get_captcha, get_pec
from src.tree import get_contact_by_crawled_page, get_result_pages, count_from_search
import csv

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
    httpSession = None
    outputFile = None

    def set_query_params(self, dove, ricerca, page=None):
        self.queryParams['dove'] = dove
        self.queryParams['ricerca'] = ricerca
        if page is not None:
            self.queryParams['page'] = page

    def scrape_page(self, page):

        # in case of page 1 we'll use risultati_globale.jsp
        # if page is > 1 we'll use pagCaptcha.jsp

        print("[OPEN PAGE] %d" % page)
        contacts = []

        url = API_ENDPOINT + "/ricerca/risultati_globale.jsp" if page == 1 else API_ENDPOINT + "/ricerca/pagCaptcha.jsp"

        if page == 1:
            query_params = {
                'cer': 1,
                'statistiche': 'S',
                'tipoRicerca': '1',
                'indiceFiglio': '3'
            }
        else:
            query_params = {
                'tipoRicerca': '1',
                'indiceFiglio': '3',
                'indice': page,
                'pagina': 0,
                'g-recaptcha-response': ''
            }

        # only if page>2 send captcha response
        # what the fuck did they smoke
        # in Camera di Commercio ?

        if page > 2:
            query_params['g-recaptcha-response'] = get_captcha(
                url,
                self.apiKeys['api_key'],
                self.apiKeys['site_key']
            )

        response = self.httpSession.post(url, data=query_params)

        tree = html.fromstring(response.text)

        if page == 1:
            self.totResults, self.totPages = count_from_search(tree)
            print("[TOTAL RESULTS] %d" % self.totResults)
            print("[TOTAL PAGES] %d" % self.totPages)

        pages = get_result_pages(tree)
        for page in pages:
            crawled_page = self.httpSession.get("%s/%s" % (API_ENDPOINT, page))
            contact = get_contact_by_crawled_page(crawled_page.text, self.scraperFields)
            contacts.append(contact)

        return contacts

    def update_page(self):
        self.queryParams["pagina"] += 1

    def start_search(self):

        # yeah it's very important executing
        # a post request with captcha response

        self.set_query_params(self.where, self.query)
        url = API_ENDPOINT + "/ricerca/lista_globale.jsp"
        self.queryParams['g-recaptcha-response'] = get_captcha(
            url,
            self.apiKeys['api_key'],
            self.apiKeys['site_key']
        )

        if self.queryParams['g-recaptcha-response'] is None:
            raise ScraperException("Recaptcha checking failed.")

        self.httpSession.post(url, data=self.queryParams)

    def __init__(self, query=None, where=None, config=None, outputFile=None):
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
        self.outputFile = "export.csv" if outputFile is None else outputFile

        if self.httpSession is None:
            self.httpSession = requests.session()

        csvfile = open(self.outputFile, "w", encoding="utf-8")

        w = csv.DictWriter(csvfile,
                           fieldnames=self.scraperFields,
                           delimiter=';',
                           quoting=csv.QUOTE_ALL)
        w.writeheader()

        self.start_search()
        w.writerows(self.scrape_page(1))

        if self.totPages is not 1:
            for i in range(2, self.totPages + 1):
                w.writerows(self.scrape_page(i))

        csvfile.close()
