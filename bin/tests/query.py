from operator import itemgetter

from indexer import InvertedIndex
from tokenizer import DocProcessor

query = 'asian women alumni'
query = 'mary had a little lamb whos fleece was white as snow'
dproc = DocProcessor()
dproc.prep_query(query)
iidx = InvertedIndex()
rel_docs = iidx.query(dproc.tokens)

ranked_docs = sorted(rel_docs.items(), key=itemgetter(1), reverse=True)

for doc in ranked_docs[:10]:
    print doc
