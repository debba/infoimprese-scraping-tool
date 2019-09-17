from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask, AnticaptchaException
from bs4 import BeautifulSoup
import requests

URL_DEC_PEC = "http://www.infoimprese.it/impr/ricerca/captcha.jsp?codiceCaptcha=%s&pecCriptata=%s"


def get_captcha(url, api_key, site_key):
    print("[CHECKING] captcha (siteKey = %s, apiKey = %s)" % (site_key, api_key))

    try:
        client = AnticaptchaClient(api_key)
        task = NoCaptchaTaskProxylessTask(url, site_key)
        job = client.createTask(task)
        job.join()
        return job.get_solution_response()
    except AnticaptchaException as ae:
        print("[ERROR] error = %s" % str(ae))
        return None


def get_pec(url, api_key, site_key):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    dec_pec = soup.find('input', {'id': 'decPec'}).get('value')
    print("[FOUND] decPec = %s" % dec_pec)
    url_errore = soup.find('input', {'id': 'urlErrore'}).get('value')
    print("[FOUND] urlErrore = %s" % url_errore)
    captcha = get_captcha(url, api_key, site_key)
    print("[FOUND] captcha = %s", captcha)
    pec_req_url = URL_DEC_PEC % (captcha, dec_pec)
    print("URL for decrypted pec will be: %s", pec_req_url)
    r = requests.get(pec_req_url)
    return r.text
