from indexer import InvertedIndex
iidx = InvertedIndex()
sims = iidx.query(['mary', 'had', 'a', 'little', 'lamb'])
print sims
