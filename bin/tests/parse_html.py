from tokenizer import DocProcessor

dprocessor = DocProcessor()
dprocessor.parse('/home/ubuntu/eecs767/var/docsnew/Zion_National_Park.htm')
for token in dprocessor.tokens:
    print token
