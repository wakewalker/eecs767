from rq import Queue
from redis import Redis
from hashlib import md5

from crawler import WebCrawler
from tokenizer import DocProcessor
from indexer import DocList, InvertedIndex


def crawl(url):
    '''
    RQ worker function which extracts URLs from the page contents at given the
    URL, then passes new URLs to both the CRAWL and PROCESS queues for futher
    action.
    '''
    wc = WebCrawler()
    urls = wc.crawl(url)
    
    dl = DocList()
    if len(dl) < 100:
        redis_conn = Redis()
        for url in urls:
            did = md5(url).hexdigest()
            if did not in dl:
                pq = Queue('crawl', connection=redis_conn)
                pq.enqueue(process, url);
                pq = Queue('process', connection=redis_conn)
                pq.enqueue(process, url);

def process(url):
    '''
    RQ worker function which tokenizes the page contents at the given URL, then 
    passes on the document posting list to the WRITE queue for futher action.
    '''
    dl = DocList()
    if len(dl) < 100:
        did = md5(url).hexdigest()
        if did not in dl:
            dproc = DocProcessor()
            dproc.parse(url)
            plist = dproc.gen_posting_list()
    
            redis_conn = Redis()
            wq = Queue('write', connection=redis_conn)
            wq.enqueue(process, args=(
                plist,
                url
            ));

def write(plist, url):
    '''
    RQ worker function which adds the given document posting list data to the
    inverted index.
    '''
    print len(plist)
    print url
    dl = DocList()
    print len(dl)
    if len(dl) < 100:
        did = md5(url).hexdigest()

        if did not in dl:
            dl.append(url)

            iidx = InvertedIndex()
            iidx.append(plist, did)
            iidx.update()


