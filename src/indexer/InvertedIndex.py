from __future__ import division
from math import log10
import linecache
import numpy

from indexer.TermNode import TermNode


class InvertedIndex(dict):

    def __init__(self,
            tdict_path='/home/ubuntu/eecs767/var/term.dct',
            dlist_path='/home/ubuntu/eecs767/var/doc.lst'
        ):
        '''Initialize the index from the given term file.'''
        super(InvertedIndex, self).__init__() 
        self.tdict_path = tdict_path 
        self.dlist_path = dlist_path

        with open(self.tdict_path, 'r+') as tdict_file:
            line_num = 1
            for line in tdict_file:
                parts = line.split('|')
                term = unicode(parts[0], 'utf-8')
                self[term] = {'loc':line_num, 'tnode':None}
                line_num += 1

        # Count the number of documents for calculations.
        i = -1
        with open(self.dlist_path, 'r+') as dlist_file:
            for i, l in enumerate(dlist_file):
                pass
            self.dnum = i + 1


    def add_term_data(self, term, did, pos):
        '''Add term data to the index for the given term.'''
        if term in self:
            tnode = self[term]['tnode']
        else:
            tnode = TermNode(term)
        tnode.plist.append({'did':did,'pos':pos})
        tnode.tf += len(pos)
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
                tdata['pdata']
            )


    def calc_scores(self):
        '''Calculate idf and weight(w)'''
        for term in self:
            if term in self:
                if self[term]['tnode'] is None:
                    tn = self.get_term_data(term)
                tnode = self[term]['tnode']
                tnode.idf = log10(self.dnum / tnode.df)
                self[term]['tnode'] = tnode
                for p in tnode.plist:
                    p['w'] = tnode.idf * len(p['pos'])
        return


    def calc_given(self, terms):
        '''Calculate idf and weight(w)'''
        for term in terms:
            if self[term]['tnode'] is None:
                tn = self.get_term_data(term)
            tnode = self[term]['tnode']
            tnode.idf = log10(self.dnum / tnode.df)
            self[term]['tnode'] = tnode
            for p in tnode.plist:
                p['w'] = tnode.idf * len(p['pos'])


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
        with open(self.tdict_path, 'r+') as tdict_file:
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
        with open(self.tdict_path, 'w+') as tdict_file:
            # Write modified
            tdict_file.writelines(tdata)
            # Add new
            for term in terms:
                tdict_file.write('%s\n' % self[term]['tnode'].serialize())
                self[term]['loc'] = line_num
                line_num += 1
        linecache.clearcache()


    def write(self):
        '''DEPRICATED: Use append instead.'''
        with open(self.tdict_path, 'w+') as tdict_file:
            line_num = 1
            for term in self:
                tdict_file.write('%s\n' % self[term]['tnode'].serialize())
                self[term]['loc'] = line_num
                line_num += 1


    def init_index(self):
        '''DEPRICATED: __init__ handles this now.'''
        with open(self.tdict_path, 'r+') as tdict_file:
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

        plist = segments[1:]
        for posting in plist:
            pdata = posting.split(':')
            tnode.plist.append({
                'did':pdata[0],
                'pos':[int(i) for i in pdata[1].split(',')]
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

        # Remove terms which are not in the index
        mterms = set()
        for term in terms:
            if term in self:
                self.get_term_data(term)
            else:
                mterms.add(term)
        terms = terms - mterms

        # Calc scores for given terms
        self.calc_given(terms)

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
            if (denominator == 0):
                dscores[did] = 0
            else:
                dscores[did] =  numerator / denominator
        
        return dscores


    def enhanced_query(self, qterms):

        cos_sims = self.query(qterms)
        term_proxs = self.calc_term_prox(set(qterms))
        
        #for did, cos_sim in cos_sims.iteritems():
            #print '%s: %s' % (did, cos_sim)
        #print '-------'
        #for did, term_prox in term_proxs.iteritems():
            #print '%s: %s' % (did, term_prox)

        fscores = {}
        #print '-------'
        for did, cos_sim in cos_sims.iteritems():
            fscore = cos_sim * term_proxs[did]
            fscores[did] = fscore
            #print '%s: %s' % (did, fscore)

        return fscores


    def calc_term_prox(self, terms):
        docs = {}
        for term in terms:
            for p in self[term]['tnode'].plist:
                if p['did'] in docs:
                    docs[p['did']][term] = p['pos']
                else:
                    docs[p['did']] = {term: p['pos']}

        #for did, doc in docs.iteritems():
            #print '%s => %s' % (did, doc)

        scores = {}
        for did, doc_terms in docs.iteritems():
            n = len(doc_terms)
            if n == 1:
                tps = 1.0
            else:
                windows = []
                for term, positions in doc_terms.iteritems():
                    windows = self.extend_windows(windows, positions)

                w = 1000000
                for window in windows:
                    wlen = max(window)-min(window)+1
                    if wlen < w:
                        w = wlen

                #print 'log10(%s)/log10(%s)' % (n, w)
                tps = log10(n)/log10(w)

            #print '%s: %s' % (did, tps)
            scores[did] = tps
            
        return scores


    def extend_windows(self, windows, positions):
        new_windows = []
        if not windows:
            for position in positions:
                new_windows.append([position])
        for window in windows:
            for position in positions:
                new_windows.append(window + [position])
        return new_windows
