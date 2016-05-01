from tokenizer import DocProcessor

dproc = DocProcessor()
#dproc.parse('/home/ubuntu/eecs767/var/docsnew/Zion_National_Park.htm')
#dproc.parse('/home/ubuntu/eecs767/var/docs/doc1.html')
dproc.parse('https://en.wikipedia.org/wiki/Main_Page')
for token in dproc.tokens:
    print token

print '------------------'
print dproc.gen_posting_list()

#with open('/home/ubuntu/eecs767/var/output/tokens.txt', 'w') as output:
#    for token in dproc.tokens:
#        output.write('%s\n' % token.encode('utf-8'))
