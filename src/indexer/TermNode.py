
class TermNode():

    def __init__(self, term, tf=0, df=0, idf=0):
        self.term = term
        self.tf = tf
        self.df = df
        self.idf = idf
        self.plist = []

    def serialize(self):
        pl_str = ''
        for p in self.plist:
            pl_str += '>%s:%s' % (
                p['did'],
                ','.join([str(i) for i in p['pos']]),
            )
        return '%s|%s:%s%s' % (
            self.term,
            self.tf,
            self.df,
            pl_str
        )
