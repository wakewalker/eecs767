import argparse
from ConfigParser import ConfigParser

from crawler import worker


arg_parser = argparse.ArgumentParser(
    description='Begin crawling based on configuration...'
)
arg_parser.add_argument('config_file', metavar='config', nargs=1,
        help='The path to the INI configuration file.'
)
args = arg_parser.parse_args()

config = ConfigParser()
config.read(args.config_file)

with open(config.get('crawler', 'seed_url_file'), 'r') as seed_url_file:
    seed_urls = [url.strip() for url in seed_url_file.readlines()]

for url in seed_urls:
    print '-- Crawling seed URL:  %s' % url
    #worker.crawl(url, config)
