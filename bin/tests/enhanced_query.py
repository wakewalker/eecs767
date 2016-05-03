from operator import itemgetter

from indexer import InvertedIndex, DocList
from tokenizer import DocProcessor

query = 'mary had a little lamb whos fleece was white as snow'
query = 'tom colwell'
query = 'asian women alumni'
query = 'information retrieval'

dproc = DocProcessor()
dproc.prep_query(query)
iidx = InvertedIndex(
        #'/home/ubuntu/eecs767/var/ku/term.dct',
        #'/home/ubuntu/eecs767/var/ku/doc.lst',
    '/home/ubuntu/eecs767/var/wikipedia/term.dct',
    '/home/ubuntu/eecs767/var/wikipedia/doc.lst',
)
rel_docs = iidx.enhanced_query(dproc.tokens)

#for doc in rel_docs:
#    print doc

#print '-----------------'

cos_ranked_docs = sorted(rel_docs, key=itemgetter('cos_sim'), reverse=True)

#for doc in cos_ranked_docs[:10]:
    #print doc

#print '-----------------'

ranked_docs = sorted(cos_ranked_docs[:10], key=itemgetter('term_prox', 'i_win_loc'), reverse=True)

#for doc in ranked_docs:
    #print doc

dlist = DocList(
    '/home/ubuntu/eecs767/var/wikipedia/doc.lst'
)
for doc in ranked_docs[:10]:
    #    print '%s: %s' % (doc['fscore'], dlist[doc['did']]['url'])
    print '%s: CosSim: %s; TermProx: %s; WinLoc: %s' % (
        dlist[doc['did']]['url'],
        round(doc['cos_sim'], 3),
        round(doc['term_prox'], 3),
        round(1/doc['i_win_loc'])
    )
