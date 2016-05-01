split_chars = ['-', '/', ',']
term_list = ['this', 'the-other-thing', 'that']
term_list = ['the-other-thing', 'this/that', 'nothing-something/anything']
#term_list = ['this', 'that', 'the-other-thing']

for i, term in enumerate(term_list):
    psc = [sc for sc in split_chars if sc in term]
    if len(psc) > 0:
        terms = term.split(psc[0])
        del term_list[i]
        term_list[i:i] =  terms
        i -= 1

print term_list



