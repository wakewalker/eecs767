from crawler import WebCrawler

wc = WebCrawler()
urls = wc.crawl('http://www.ku.edu')
for url in urls:
    print url
len(urls)
