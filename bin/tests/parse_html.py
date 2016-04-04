from tokenizer import DocProcessor

dproc = DocProcessor()
dproc.parse('/home/ubuntu/eecs767/var/docsnew/Zion_National_Park.htm')
#for token in dproc.tokens:
#    print token

with open('/home/ubuntu/eecs767/var/output/tokens.txt', 'w') as output:
    for token in dproc.tokens:
        output.write('%s\n' % token.encode('utf-8'))
