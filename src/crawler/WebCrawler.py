import requests
from urlparse import urlparse, urldefrag, urljoin
from BeautifulSoup import BeautifulSoup

class WebCrawler():

    def crawl(self, target_url):
        requests.packages.urllib3.disable_warnings()
        target_attrs = urlparse(target_url)
        resp = requests.get(target_url)

        soup = BeautifulSoup(resp.text)
        
        urls = set([])
        for a in soup.findAll('a', href=True):
            # Remove fragmentation identifiers
            url = urldefrag(a['href'])[0]
            urlattrs = urlparse(url)
            # Transform relative path URL
            if urlattrs.scheme == '':
                    url = urljoin(target_url, url)
            # Ignore mailto and tel links
            if urlattrs.scheme not in ['mailto', 'tel']:
                urls.add(url)

        return urls
