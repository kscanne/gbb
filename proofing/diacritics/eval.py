import os.path
import urllib.request
import zipfile
import diacritization_stripping_data
#from nltk.tokenize import word_tokenize

def word_tokenize(s):
  return s.split(' ')

def stripDiacritics(s):
  m = diacritization_stripping_data.strip_diacritization_uninames
  return ''.join(  map(lambda c: m.get(c,c), s))

def readCorpusFromFile(fileName):
  with open(fileName, "r", encoding="utf-8") as f:
    return [line.rstrip() for line in f]

def retrieveDataset():
  if not all(os.path.exists(x+'-clean.txt') for x in ('dev','test','train')):
    zipfileName = 'tuairisc-2015.zip'
    if not os.path.exists(zipfileName):
      zipURL = 'https://cs.slu.edu/~scannell/gbb/'+zipfileName
      urllib.request.urlretrieve(zipURL, zipfileName)
    with zipfile.ZipFile(zipfileName, 'r') as zipRef:
      zipRef.extractall()

def score(predictedCorpus, goldCorpus):
  totalWords = 0
  correctWords = 0
  for predictedSent, goldSent in zip(predictedCorpus, goldCorpus):
    for p, g in zip(word_tokenize(predictedSent), word_tokenize(goldSent)):
      totalWords += 1
      if p == g:
        correctWords += 1
  return correctWords/totalWords

def restoreIdentity(train, dev, stripped):
  return stripped

def restoreUnigrams(train, dev, stripped):
  unigrams = dict()
  for trainSent in train:
    for t in word_tokenize(trainSent):
      asciiToken = stripDiacritics(t)
      if not asciiToken in unigrams:
        unigrams[asciiToken] = dict()
      unigrams[asciiToken][t] = unigrams[asciiToken].get(t,0) + 1
  bestRestoration = dict()
  for k in unigrams:
    bestCount = 0
    for cand in unigrams[k]:
      if unigrams[k][cand] > bestCount:
        bestRestoration[k] = cand
        bestCount = unigrams[k][cand]
  ans = []
  for strippedSent in stripped:
    restoredTokens = []
    for t in word_tokenize(strippedSent):
      restoredTokens.append(bestRestoration.get(t, t))
    ans.append(' '.join(restoredTokens))
  return ans

def evaluateAll(algorithms):
  ans = dict()
  retrieveDataset()
  trainCorpus = readCorpusFromFile('train-clean.txt')
  devCorpus = readCorpusFromFile('dev-clean.txt')
  testCorpus = readCorpusFromFile('test-clean.txt')
  strippedCorpus = list(map(stripDiacritics, testCorpus)) 
  for k in algorithms:
    predictions = algorithms[k](trainCorpus, devCorpus, strippedCorpus)
    ans[k] = score(predictions, testCorpus)
  return ans

def main():
  results = evaluateAll({
    'Keep as ASCII': restoreIdentity,
    'Unigrams': restoreUnigrams,
  })
  for p in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(p[0]+':', p[1])

main()
