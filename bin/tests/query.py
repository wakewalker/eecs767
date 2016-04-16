from indexer import InvertedIndex
iidx = InvertedIndex()
#sims = iidx.query(['mary', 'had', 'a', 'little', 'lamb'])
sims = iidx.query(['alumni', 'donate'])
print sims
