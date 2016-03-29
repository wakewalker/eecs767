from InvertedIndex import InvertedIndex
import csv
from sys import exit

tdict = InvertedIndex()
tdict.init_index()
for term in sorted(tdict):
    print '(%s) %s' % (tdict[term]['loc'], term)

