

class InvertedIndex():
    '''This object acts as an inverted index...'''

    index_fp = '/home/ubuntu/eecs767/var/term.inx'
    dict_fp = '/home/ubuntu/eecs767/var/term.dct'
    posting_fp = '/home/ubuntu/eecs767/var/term.pst'

    tdict = TermDict()

    def __init__(self, config_fp):
        '''Constructor...'''

        #Get filepaths from config

        # If target files don't exist, create them
        return


    def build(self, term_list):
        '''
        Build an inverted index given a list of term-document associations.

        WARNING: This method will re-write the existing inverted index files!
        '''

        # Generate dictionary and posting objects
        self.tdict.build(term_list)

        # Write to files
        self.tdict.write(
            self.index_fp,
            self.dict_fp,
            self.posting_fp
        )
        

    def init_index(self):
        '''Pull the term index into memory for effective searching.'''
        return
