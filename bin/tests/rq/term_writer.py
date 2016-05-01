from tokenizer import DocProcessor
from crawler import worker
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('/home/ubuntu/eecs767/etc/config/wikipedia.ini')

url = 'https://en.wikipedia.org/wiki/Main_Page'
dproc = DocProcessor()
dproc.parse(url)
plist = dproc.gen_posting_list()

worker.write(plist, url, config)
