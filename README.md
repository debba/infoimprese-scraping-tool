### InfoImprese Scraper Bot 

**Config**

Before using for the first time this tool you should create a config.json inside the conf folder.
Please take a look to conf/config.example.json or directly clone it.

You can setup an *Anti-Captcha* API keys in order to skip captcha checks,
please follow how to generate keys from this link:
https://anti-captcha.com

You can setup fields you want to export. 
A complete list:

- "Denominazione",
- "Sede legale",
- "Attività",
- "Sede operativa",
- "Indirizzo web",
- "Posta elettronica",
- "Commercio elettronico",
- "Chi siamo",
- "Cosa facciamo",
- "Classe di fatturato",
- "Canali di vendita",
- "Marchi",
- "Principali paesi di export",
- "Certificazioni"

You can setup a mode, you can learn about it following the next section.

**Modes**
You can choose one of the following scraping modes:

- _search_by_name_ (_Ricercando nel Nome_ in the website)
- _search_by_desc_ (_Ricercando nella Descrizione attività	_ in the website)
- _with_dash_ (_con la Vetrina su infoimprese.it_ in the website)
- _with_cert_ (_con certificazione di qualità_ in the website)
- _with_dash_ (_che praticano e-commerce_ in the website)
- _with__email_ (_che possiedono l'e-mail_ in the website)
- _with_website_ (_che hanno il sito internet_ in the website)
- _with_export_ (_che svolgono attività di export_ in the website)

**Usage**

```
usage: main.py [-h] -q QUERY [-m MODE] [-l LOCATION] [-o OUTPUT]
```

Arguments are:
- *query* represents your keyword
- *location* represents where you want search
- *mode* represent modes (check Modes section)
- *output* csv file for storing data

Enjoy :)
