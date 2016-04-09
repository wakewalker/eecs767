from tokenizer import DocProcessor
from indexer import InvertedIndex

docs = {
    1: '/home/ubuntu/eecs767/var/docs/doc1.html',
    2: '/home/ubuntu/eecs767/var/docs/doc2.html',
    3: '/home/ubuntu/eecs767/var/docs/doc3.html',
    4: '/home/ubuntu/eecs767/var/docs/doc4.html',
    5: '/home/ubuntu/eecs767/var/docs/doc5.html',
}

dproc = DocProcessor()
iidx = InvertedIndex()

for did, doc in docs.iteritems():
    print '-- Processing Doc #%s: %s' % (did, doc)
    dproc.parse(doc)
    plist = dproc.gen_posting_list()
    
    iidx.append(plist, did)
#    iidx.calc_scores()
    iidx.update()
#    iidx.clear()
