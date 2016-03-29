from __future__ import division
from math import log10
from linecache import getline

class TermNode():

    def __init__(self, term, tf=0, df=0, idf=0):
        self.term = term
        self.tf = tf
        self.df = df
        self.idf = idf
        self.plist = []


class InvertedIndex(dict):

    def __init__(self, tdict_path='/home/ubuntu/eecs767/var/term.dct'):
        self.tdict_path = tdict_path
        # TODO: Get dictionary filepath from config
        super(InvertedIndex, self).__init__()

    def add_term_data(self, term, did, tf):
        if term in self:
            tnode = self[term]['tnode']
        else:
            tnode = TermNode(term)
        tnode.plist.append({'did':did,'tf':int(tf)})
        tnode.tf += int(tf)
        tnode.df += 1
        self[term] = {'loc':None, 'tnode':tnode}

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
            tnode = self[term]['tnode']
            tnode.idf = log10(dnum / tnode.df)
            self[term]['tnode'] = tnode
            for p in tnode.plist:
                p['w'] = tnode.idf * p['tf']
        
    def write(self):
        tdict_file = open(self.tdict_path, 'w')
        line_num = 1
        for term in self:
            tnode = self[term]['tnode']
            pl_str = ''
            for p in tnode.plist:
                pl_str += '>%s:%s:%s' % (p['did'],p['tf'],p['w'])
            tdict_file.write('%s|%s:%s:%s%s\n' % (
                term,
                tnode.tf,
                tnode.df,
                tnode.idf,
                pl_str
            ))
            self[term]['loc'] = line_num
            line_num += 1
        tdict_file.close()

    def init_index(self):
        with open(self.tdict_path, 'r') as tdict_file:
            line_num = 1
            for line in tdict_file:
                parts = line.split('|')
                term = parts[0]
                self[term] = {'loc':line_num, 'tnode':None}
                line_num += 1
        tdict_file.close()


    def get_term_data(term):
        tdata = getline(
            self.tdict_path,
            self[term]['loc']
        )

        return


    def clear(clear):
        '''Clear term dictionary tnodes from memory'''
        return



