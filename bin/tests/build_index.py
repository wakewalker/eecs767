from indexer import InvertedIndex
import csv
from sys import exit

with open('/home/ubuntu/eecs767/var/sample.csv') as f:
    term_list = []
    for row in csv.DictReader(f, skipinitialspace=True):
        term_list.append(row)

tdict = InvertedIndex()
tdict.build(term_list)
tdict.write()

for term in sorted(tdict):
    tnode = tdict[term]['tnode']
    pl_str = ''
    for p in tnode.plist:
        pl_str += ' -> %s x %s (%.3f)' % (p['did'], p['tf'], p['w'])
    print '(%s) %s (tf:%s; df:%s; idf:%.3f):%s' % (
        tdict[term]['loc'],
        tnode.term,
        tnode.tf,
        tnode.df,
        tnode.idf,
        pl_str
    )
