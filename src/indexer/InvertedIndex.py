from __future__ import division
from math import log10
import linecache
import numpy

from indexer.TermNode import TermNode


class InvertedIndex(dict):

    dnum = 5

    def __init__(self, tdict_path='/home/ubuntu/eecs767/var/term.dct'):
        '''Initialize the index from the given term file.'''
        super(InvertedIndex, self).__init__()
        # TODO: Get dictionary filepath from config
        self.tdict_path = tdict_path 
        with open(self.tdict_path, 'r') as tdict_file:
            line_num = 1
            for line in tdict_file:
                parts = line.split('|')
                term = unicode(parts[0], 'utf-8')
                self[term] = {'loc':line_num, 'tnode':None}
                line_num += 1


    def add_term_data(self, term, did, tf):
        '''Add term data to the index for the given term.'''
        if term in self:
            tnode = self[term]['tnode']
        else:
            tnode = TermNode(term)
        tnode.plist.append({'did':did,'tf':int(tf)})
        tnode.tf += int(tf)
        tnode.df += 1
        if term in self:
            self[term]['tnode'] = tnode
        else:
            self[term] = {'loc':None, 'tnode':tnode}


    def append(self, tlist, did):
        '''Append term data to the inverted index for the given document.'''
        for tdata in tlist:
            term = tdata['term']

            # 1. Get term data if not in memory
            if (term in self) and (self[term]['tnode'] is None):
                self.get_term_data(tdata['term'])

            # 2. Add term data
            self.add_term_data(
                tdata['term'],
                did,
                tdata['tfreq']
            )


    def calc_scores(self):
        '''Calculate idf and weight(w)'''
        for term in self:
            if self[term]['tnode'] is None:
                self.get_term_data(term)
            tnode = self[term]['tnode']
            tnode.idf = log10(self.dnum / tnode.df)
            self[term]['tnode'] = tnode
            for p in tnode.plist:
                p['w'] = tnode.idf * p['tf']
        return


    def build(self, term_list):
        '''DEPRICATED: Use append instead.'''
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


    def update(self):
        '''Write the in-memory tnodes to file.'''
        with open(self.tdict_path, 'r') as tdict_file:
            tdata = tdict_file.readlines()
            line_num = len(tdata) + 1

        # Get updated / new terms
        terms = {}
        for term in self:
            if (term in self) and (self[term]['tnode'] is not None):
                terms[term] = self[term]

        # Modify existing term data in tdata
        for term in terms.keys():
            if self[term]['loc'] is not None:
                tdata[self[term]['loc']-1] = (
                        '%s\n' % self[term]['tnode'].serialize()
                )
                del terms[term]

        # Write changes to file
        with open(self.tdict_path, 'w') as tdict_file:
            # Write modified
            tdict_file.writelines(tdata)
            # Add new
            for term in terms:
                tdict_file.write('%s\n' % self[term]['tnode'].serialize())
                self[term]['loc'] = line_num
                line_num += 1
        linecache.clearcache()


    def write(self):
        '''DEPRICATED: Use write_to_file instead.'''
        with open(self.tdict_path, 'w') as tdict_file:
            line_num = 1
            for term in self:
                tdict_file.write('%s\n' % self[term]['tnode'].serialize())
                self[term]['loc'] = line_num
                line_num += 1


    def init_index(self):
        '''DEPRICATED: __init__ handles this now.'''
        with open(self.tdict_path, 'r') as tdict_file:
            line_num = 1
            for line in tdict_file:
                parts = line.split('|')
                term = parts[0]
                self[term] = {'loc':line_num, 'tnode':None}
                line_num += 1


    def get_term_data(self, term):
        '''
        Retrieves term data from dictionary file for the given term.
        TODO: Clean this up.
        '''
        if term not in self:
            return False
        if 'loc' not in self[term]:
            return False

        tdata = linecache.getline(
            self.tdict_path,
            self[term]['loc']
        ).rstrip()
        segments = tdata.split('|')
        term = segments[0]
        tnode = TermNode(term)

        segments = segments[1].split('>')
        tinfo = segments[0].split(':')
        tnode.tf = int(tinfo[0])
        tnode.df = int(tinfo[1])
        tnode.idf = float(tinfo[2])

        plist = segments[1:]
        for posting in plist:
            pdata = posting.split(':')
            tnode.plist.append({
                'did':pdata[0],
                'tf':int(pdata[1]),
                'w':float(pdata[2])
            })

        self[term]['tnode'] = tnode
        return tnode


    def clear(self):
        '''
        Clear term dictionary tnodes from memory.
        TODO: This isn't working correctly for some reason.
        '''
        for term in self:
            self[term]['tnode'] = None


    def query(self, qterms):
        '''Initial pass a calculating similarity scores from query tokens.'''
        terms = set(qterms)
        docs = []
        tdata = {}

        # Remove term which are not in the index
        mterms = set()
        for term in terms:
            if term in self:
                self.get_term_data(term)
            else:
                mterms.add(term)
        terms = terms - mterms

        # Prep term data for building term-document matrix
        qv = []
        for term in terms:
            qv.append(self[term]['tnode'].idf)
            if term in self:
                tdata[term] = {}
                for p in self[term]['tnode'].plist:
                    if p['did'] not in docs:
                        docs.append(p['did'])
                    tdata[term][p['did']] = p['w']

        # Build term-document matrix
        matrix = []
        for tidx, term in enumerate(terms):
            matrix.append([])
            for didx, did in enumerate(docs):
                if did in tdata[term]:
                    matrix[tidx].append(tdata[term][did])
                else:
                    matrix[tidx].append(0)
        
        # Create numpy "matrix" for linear algebra calcs
        matrix = numpy.array(matrix).T

        # Calculate cosine similarity
        dscores = {}
        for didx, did in enumerate(docs):
            dv = matrix[didx,:]
            numerator = numpy.dot(qv, dv)
            denominator = numpy.linalg.norm(qv) * numpy.linalg.norm(dv)
            dscores[did] =  numerator / denominator
        
        return dscores

