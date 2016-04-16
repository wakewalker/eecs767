from crawler import worker

urls = [
    'http://www.ku.edu',
    'http://www.kumc.edu',
    'http://www.eecs.ku.edu',
    'http://www.engr.ku.edu',
    'http://www.edwardscampus.ku.edu/',
]

for url in urls:
    worker.process(url)
