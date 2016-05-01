from crawler import WebCrawler

wc = WebCrawler()
urls = wc.crawl('https://en.wikipedia.org/wiki/Main_Page')
for url in urls:
    print url
len(urls)
