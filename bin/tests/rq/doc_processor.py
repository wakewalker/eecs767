from crawler import worker

urls = [
    'http://www.ku.edu',
    'http://www.kumc.edu',
    'http://www.eecs.ku.edu',
    'http://www.engr.ku.edu',
    'http://www.edwardscampus.ku.edu/',
]

for url in urls:
    print '-- Processing %s' % url
    worker.process(url)
