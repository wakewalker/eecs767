from tokenizer import DocProcessor
from crawler import worker

url = 'http://www.kumc.edu'
dproc = DocProcessor()
dproc.parse(url)
plist = dproc.gen_posting_list()

worker.write(plist, url)
