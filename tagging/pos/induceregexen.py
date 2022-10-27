import re

#targetPrecision = 0.95   # ignore suffixes that don't map to tag > this %
#prune = 200   # ignore suffixes that appear fewer than this number of times
#fileName = 'datasets/iudt-dict.tsv'

targetPrecision = 0.90
prune = 100
fileName = 'datasets/iudt-full-dict.tsv'

with open(fileName, "r", encoding="utf-8") as f:
    ans = [tuple(line.rstrip().split('\t')) for line in f]

rules = dict()
for suffixLength in range(1,6):
  cands = dict()
  for pair in ans:
    if len(pair[0])>=suffixLength:
      c = pair[0][-suffixLength:]
      cands[c] = 1 + cands.get(c,0)
  for c in cands:
    if cands[c] < prune or any(c[-len(prev):]==prev for prev in rules):
      continue
    tagCount = dict()
    total = 0
    for pair in ans:
      if pair[0][-suffixLength:]==c:
        total += 1
        tagCount[pair[1]] = 1+tagCount.get(pair[1],0)
    if total>20:
      topTag = max(tagCount, key=tagCount.get)
      precision = tagCount[topTag]/total
      #print("suff=",c,";toptag=",topTag,";precision=",precision)
      if precision > targetPrecision:
        rules[c] = topTag

for r in rules:
  print(r+'\t'+rules[r])
