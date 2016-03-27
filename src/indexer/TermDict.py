from __future__ import division
from math import log10

class TermNode():

    def __init__(self, term, tf=0, df=0, idf=0):
        self.term = term
        self.tf = tf
        self.df = df
        self.idf = idf
        self.plist = {}


class TermDict(dict):

    def add_term_data(self, term, did, tf):
        if term in self:
            tnode = self[term]
        else:
            tnode = TermNode(term)
        tnode.plist[did] = tf
        tnode.tf += int(tf)
        tnode.df += 1
        self[term] = tnode

    def build(self, term_list):
        # Build term dictionary and posting lists.
        dids = []
        for term_info in term_list:
            if term_info['did'] not in dids:
                dids.append(term_info['did'])

            self.add_term_data(
                term_info['term'],
                term_info['did'],
                term_info['tfreq']
            )
        dnum = len(dids)

        # Calculate idf and weight(w)
        for term in self:
            tnode = self[term]
            tnode.idf = log10(dnum / tnode.df)
            self[term] = tnode
        
        


    def write(index_fp, dict_fp, posting_fp):
        tindx = open(index_fp, 'w')
        tdict = open(dict_fp, 'w')
        tpost = open(posting_fp, 'w')

        tindx.close()
        tdict.close()
        tpost.close()
