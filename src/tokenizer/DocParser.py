from urllib2 import urlopen
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, Tag
import sys

class DocParser():

    blacklist = [u'script']
    stoplist = [':', '.', ':', ';', '(', ')', '[', ']']
   
    def parse(self, doc_src):
        self.doc_src = doc_src
        if self.is_url(doc_src):
            html = urlopen(doc_src)
        else:
            with open(doc_src, 'r') as local_file:
                html = local_file.read()

        self.extract_tokens(html)
        self.normalize_tokens()


    def is_url(self, doc_src):
        parsed_url = urlparse(doc_src)
        return bool(parsed_url.scheme)


    def extract_tokens(self, html):
        soup = BeautifulStoneSoup(
            html,
            convertEntities=BeautifulStoneSoup.ALL_ENTITIES
        )
        body = soup.find('body')
        tokens = self.find_tokens(body)
        self.tokens = tokens


    def find_tokens(self, node):
        tokens = []
        if isinstance(node, Tag):
            if node.name not in self.blacklist:
                for child in node.contents:
                    tokens.extend(self.find_tokens(child))
        else:
            tokens = node.string.split()
        return tokens

    def normalize_tokens(self):
        self.tokens = [ token.lower() for token in self.tokens if token not in self.stoplist]
