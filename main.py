import json
import os

from src.infoimprese import Scraper, ScraperException

CONFIG_FILE = "conf/config.json"

if __name__ == "__main__":

    if not os.path.exists(CONFIG_FILE):
        print("No config file found. Exit.")
        exit(0)

    f = open(CONFIG_FILE)
    config = json.load(f)

    try:
        Scraper(query="ottica", where="milano", api_keys=config['anticaptcha'])
    except ScraperException as se:
        print("Error: " + str(se))
