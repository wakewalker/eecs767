from rq import Queue
from redis import Redis
from hashlib import md5
from time import sleep
from urlparse import urlsplit

from crawler import WebCrawler
from tokenizer import DocProcessor
from indexer import DocList, InvertedIndex


def crawl(url, config, skip_delay=False):
    '''
    RQ worker function which extracts URLs from the page contents at given the
    URL, then passes new URLs to both the CRAWL and PROCESS queues for futher
    action.
    '''

    DELAY = int(config.get('crawler', 'crawl_delay'))
    MAX_DOCS = int(config.get('crawler', 'max_docs'))
    FRNT_LIST_FILE = config.get('crawler', 'url_frontier_file')
    TARGET_DOMAIN = config.get('crawler', 'target_domain')

    if not skip_delay:
        sleep(float(DELAY))

    wc = WebCrawler()
    urls = wc.crawl(url)
    
    dl = DocList(FRNT_LIST_FILE)
    if len(dl) < MAX_DOCS:
        redis_conn = Redis()
        for url in urls:
            did = md5(url).hexdigest()
            domain = urlsplit(url).netloc
            if (did not in dl) and (domain == TARGET_DOMAIN):
                dl.append(url)
                cq = Queue('crawl', connection=redis_conn)
                cq.enqueue(crawl, args=(
                    url,
                    config
                ));
                pq = Queue('process', connection=redis_conn)
                pq.enqueue(process, args=(
                    url,
                    config
                ));


def process(url, config):
    '''
    RQ worker function which tokenizes the page contents at the given URL, then 
    passes on the document posting list to the WRITE queue for futher action.
    '''
    MAX_DOCS = int(config.get('crawler', 'max_docs'))
    DOC_LIST_FILE = config.get('indexer', 'doc_list_file')
    
    dl = DocList(DOC_LIST_FILE)
    if len(dl) < MAX_DOCS:
        did = md5(url).hexdigest()
        if did not in dl:
            dproc = DocProcessor()
            dproc.parse(url)
            plist = dproc.gen_posting_list()
    
            redis_conn = Redis()
            wq = Queue('write', connection=redis_conn)
            wq.enqueue(write, args=(
                plist,
                url,
                dproc.title,
                config
            ));


def write(plist, url, title, config):
    '''
    RQ worker function which adds the given document posting list data to the
    inverted index.
    '''
    MAX_DOCS = int(config.get('crawler', 'max_docs'))
    TERM_DICT_FILE = config.get('indexer', 'term_dict_file')
    DOC_LIST_FILE = config.get('indexer', 'doc_list_file')
    
    dl = DocList(DOC_LIST_FILE)
    if len(dl) < MAX_DOCS:
        did = md5(url).hexdigest()

        if did not in dl:
            dl.append(url, title)

            iidx = InvertedIndex(
                TERM_DICT_FILE,
                DOC_LIST_FILE
            )
            iidx.append(plist, did)
            iidx.update()


