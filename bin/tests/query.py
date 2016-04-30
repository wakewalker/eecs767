from operator import itemgetter

from indexer import InvertedIndex, DocList
from tokenizer import DocProcessor

query = 'asian women alumni'
query = 'mary had a little lamb whos fleece was white as snow'
query = 'tom colwell'
query = 'information retrieval'

dproc = DocProcessor()
dproc.prep_query(query)
iidx = InvertedIndex(
    '/home/ubuntu/eecs767/var/ku/term.dct',
    '/home/ubuntu/eecs767/var/ku/doc.lst',
)
rel_docs = iidx.query(dproc.tokens)

ranked_docs = sorted(rel_docs.items(), key=itemgetter(1), reverse=True)

dlist = DocList(
    '/home/ubuntu/eecs767/var/ku/doc.lst'
)
for doc in ranked_docs[:10]:
    print '%s: %s' % (doc[1], dlist[doc[0]])
