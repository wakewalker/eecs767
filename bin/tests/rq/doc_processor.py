from crawler import worker
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('/home/ubuntu/eecs767/etc/config/wikipedia.ini')

urls = [
    #'http://www.ku.edu',
    #'http://www.kumc.edu',
    #'http://www.eecs.ku.edu',
    #'http://www.engr.ku.edu',
    #'http://www.edwardscampus.ku.edu/',
    'https://en.wikipedia.org/wiki/Main_Page'
]

for url in urls:
    print '-- Processing %s' % url
    worker.process(url, config)
