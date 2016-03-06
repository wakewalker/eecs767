

class PostingList():

    def __init__(self, head=None):
        self.head = head

    def insert(self, doc_id, doc_freq): 
        posting = Posting(doc_id, doc_freq, self.head)
        self.head = posting

    def length(self):
        counting = self.head
        count = 0
        while counting:
            count += 1
            counting = counting.get_next()
        return count


class Posting():

    def __init__(self, doc_id=None, doc_freq=None, next_posting=None):
        self.doc_id = doc_id
        self.doc_freq = doc_freq
        self.next_posting = next_posting

    def set_next(self, next_posting):
        self.next_posting = next_posting

    def get_freq(self):
        return self.doc_freq

    def get_next(self):
        return self.next_posting
