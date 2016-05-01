from operator import itemgetter

from indexer import InvertedIndex, DocList
from tokenizer import DocProcessor

query = 'mary had a little lamb whos fleece was white as snow'
query = 'tom colwell'
query = 'information retrieval'
query = 'asian women alumni'

dproc = DocProcessor()
dproc.prep_query(query)
iidx = InvertedIndex(
        #'/home/ubuntu/eecs767/var/ku/term.dct',
        #'/home/ubuntu/eecs767/var/ku/doc.lst',
    '/home/ubuntu/eecs767/var/wikipedia/term.dct',
    '/home/ubuntu/eecs767/var/wikipedia/doc.lst',
)
rel_docs = iidx.query(dproc.tokens)
#print rel_docs.items()

ranked_docs = sorted(rel_docs.items(), key=itemgetter(1), reverse=True)
#print ranked_docs[:10]

dlist = DocList(
    '/home/ubuntu/eecs767/var/wikipedia/doc.lst'
)
for doc in ranked_docs[:10]:
    print '%s: %s' % (doc[1], dlist[doc[0]])
