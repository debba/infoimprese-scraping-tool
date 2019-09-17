import json
import os
from src.infoimprese import Scraper, ScraperException
import argparse

CONFIG_FILE = "conf/config.json"

if __name__ == "__main__":

    if not os.path.exists(CONFIG_FILE):
        print("No config file found. Exit.")
        exit(0)

    f = open(CONFIG_FILE)
    config = json.load(f)

    mode = 'search_by_name'
    if config['scraper'] and config['scraper']['mode'] :
        mode = config['scraper']['mode']

    parser = argparse.ArgumentParser(description='Extract data from Infoimprese')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-q', '--query', type=str, help='Activites to scrape in Infoimprese', required=True)
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-m', '--mode', type=str, help='Mode', default=mode)
    optional.add_argument('-l', '--location', type=str, help='Location (it could be a region, city, address etc.)')
    optional.add_argument('-o', '--output', type=str, help='Output file', default="export.csv")

    args = parser.parse_args()

    config['scraper']['mode'] = args.mode

    try:
        Scraper(query=args.query, where=args.location, config=config, output_file=args.output)
    except ScraperException as se:
        print("Error: " + str(se))
