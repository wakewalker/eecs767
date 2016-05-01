from urllib2 import urlopen
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup, Tag, Comment
import sys
import snowballstemmer

class DocProcessor():

    blacklist = [u'script']
    stopwords = ['a', 'an', 'of', 'in', 'is', 'on', 'to', 'at', 'the']
    stopchars = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '{', '[', '}', ']', '|', '\\', ':', ';', '"', '\'', '<', ',', '>', '.', '?', '/', u'\ufffd', u'\u2265', u'\u2014', u'\u2022', u'\u00ae', u'\ufeff', u'\xbb', u'\xc2', u'\xb0']
    splitchars = ['-', '/', '\'']


    def __init__(self):
        self.stoplist = self.stopwords + self.stopchars


    def parse(self, doc_src):
        self.doc_src = doc_src
        if self.is_url(doc_src):
            html = urlopen(doc_src)
        else:
            with open(doc_src, 'r') as local_file:
                html = local_file.read()

        self.extract_tokens(html)
        self.process_tokens()


    def prep_query(self, query):
        self.tokens = query.split()
        self.process_tokens()


    def process_tokens(self):
        self.split_tokens()
        self.normalize_tokens()
        stemmer = snowballstemmer.stemmer('english')
        self.tokens = stemmer.stemWords(self.tokens)


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
        elif not isinstance(node, Comment):
            tokens = [token.strip() for token in node.string.split()]
        return tokens


    def split_tokens(self):
        for i, token in enumerate(self.tokens):
            splitchars = [sc for sc in self.stopchars if sc in token]
            if len(splitchars) > 0:
                tokens = token.split(splitchars[0])
                del self.tokens[i]
                self.tokens[i:i] = tokens
                i -= 1


    def normalize_tokens(self):
        self.tokens = [self.normalize(token) for token in self.tokens if token not in self.stoplist]
        self.tokens = [token for token in self.tokens if token is not None]
        self.tokens = [token.encode('UTF-8') for token in self.tokens]


    def normalize(self, token):
        token = token.lower()
        token = self.char_strip(token)
        return token

    
    def char_strip(self, otoken):
        '''Strip leading and trailing stopchars recusively'''
        token = otoken
        if len(token) > 0 and token[0] in self.stopchars:
            token = token[1:]
        if len(token) > 0 and token[-1] in self.stopchars:
            token = token[:-1]
        
        if token == '':
            return None
        elif token == otoken:
            return token
        else:
            return self.char_strip(token)


    def gen_posting_list(self):
        pdict = {}
        for pos, token in enumerate(self.tokens):
            if token in pdict:
                pdict[token].append(pos)
            else:
                pdict[token] = [pos]

        plist = []
        for term in sorted(pdict):
            plist.append({
                'term': term,
                'pdata': pdict[term]
            })

        return plist



