from tokenizer import DocParser

dparser = DocParser()
dparser.parse('/home/ubuntu/eecs767/var/docsnew/Zion_National_Park.htm')
for token in dparser.tokens:
    print token
