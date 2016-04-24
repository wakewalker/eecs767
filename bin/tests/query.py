from operator import itemgetter

from indexer import InvertedIndex
iidx = InvertedIndex()
rel_docs = iidx.query(['asian', 'women', 'alumni'])

ranked_docs = sorted(rel_docs.items(), key=itemgetter(1), reverse=True)

for doc in ranked_docs[:10]:
    print doc
