import snowballstemmer

tokens = ['mary', 'had', 'a', 'little', 'lamb', 'whos', 'fleece', 'was', 'white', 'as', 'snow']
tokens = ['This-Is a/test', 'Of', 'wHat', 'thiS', 'STEMMER', 'is', 'possible', 'of', 'bitch\'s']
stemmer = snowballstemmer.stemmer('english')
tokens = [stemmer.stemWord(token) for token in tokens]
print tokens
print stemmer.stemWords(tokens)

