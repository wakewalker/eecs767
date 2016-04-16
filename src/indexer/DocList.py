from hashlib import md5


class DocList(dict):

    def __init__(self, dlist_path='/home/ubuntu/eecs767/var/doc.lst'):
        super(DocList, self).__init__()
        # TODO: Get document list filepath from config.
        self.dlist_path = dlist_path
        with open(self.dlist_path, 'r+') as dlist_file:
            for line in dlist_file.readlines():
                segments = line.rstrip().split('|')
                self[segments[0]] = segments[1]

    def append(self, url):
        did = md5(url).hexdigest()

        if did not in self:
            self[did] = url
        
            with open(self.dlist_path, 'a+') as dlist_file:
                dlist_file.write('%s|%s\n' % (did, url))
