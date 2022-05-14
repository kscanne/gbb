import os
import urllib.request
import ssl
import zipfile
import lzma
import pickle
import re
import diacritization_stripping_data as dsd
from nltk.tokenize import word_tokenize, NLTKWordTokenizer

def mkdir_p(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)

def slugify(name):
  pattern = re.compile(r'[^A-Za-z]')
  return re.sub(pattern, '', name)

def stripDiacritics(s):
  return ''.join(map(lambda c: dsd.strip_diacritization_uninames.get(c,c), s))

def hasDiacritics(s):
  return any(c in dsd.strip_diacritization_uninames for c in s)

def writeCorpusToFile(corpus, fileName):
  with open(fileName, "w", encoding="utf-8") as f:
    for sent in corpus:
      f.write(sent+'\n')

def readCorpusFromFile(fileName):
  with open(fileName, "r", encoding="utf-8") as f:
    return [line.rstrip() for line in f]

def readCorpusFromXZFile(fileName):
  return lzma.open(fileName).read().decode('utf-8').splitlines()

# because SLU systems are awful
def urlRetrieveNoSSL(url, fileName):
  with urllib.request.urlopen(url, context=ssl.SSLContext()) as u, \
                        open(fileName, 'wb') as f:
    f.write(u.read())

def retrieveDataset(name, dataDir):
  ans = {'slug' : name}
  files = ('dev','test','train')
  if name == 'tuairisc':
    if not all(os.path.exists(dataDir+x+'-clean.txt') for x in files):
      zipfileName = 'tuairisc-2015.zip'
      if not os.path.exists(dataDir+zipfileName):
        zipURL = 'https://cs.slu.edu/~scannell/gbb/'+zipfileName
        urlRetrieveNoSSL(zipURL, dataDir+zipfileName)
      with zipfile.ZipFile(dataDir+zipfileName, 'r') as zipRef:
        zipRef.extractall(path=dataDir)
    for x in files:
      ans[x] = readCorpusFromFile(dataDir+x+'-clean.txt')
  elif name == 'charles':
    if not all(os.path.exists(dataDir+'ga/target_'+x+'.txt.xz') for x in files):
      zipfileName = 'ga.zip'
      if not os.path.exists(dataDir+zipfileName):
        zipURL = 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2607/ga.zip?sequence=1&isAllowed=y'
        urllib.request.urlretrieve(zipURL, dataDir+zipfileName)
      with zipfile.ZipFile(dataDir+zipfileName, 'r') as zipRef:
        zipRef.extractall(path=dataDir)
    for x in files:
      ans[x] = readCorpusFromXZFile(dataDir+'ga/target_'+x+'.txt.xz')
  else:
    sys.exit("Unknown dataset\n")
  return ans

# returns a tuple: (WLA, Precision, Recall)
# Precision/Recall is for finding missing diacritics
def score(predictedCorpus, goldCorpus):
  totalWords = 0
  correctWords = 0
  totalDiacritics = 0
  predictedDiacritics = 0
  correctDiacritics = 0
  for predictedSent, goldSent in zip(predictedCorpus, goldCorpus):
    for p, g in zip(word_tokenize(predictedSent), word_tokenize(goldSent)):
      totalWords += 1
      if p == g:
        correctWords += 1
      if hasDiacritics(g):
        totalDiacritics += 1
        if p == g:
          correctDiacritics += 1
      if hasDiacritics(p):
        predictedDiacritics += 1
      
  wla = 100*correctWords/totalWords
  precision = float('nan')
  if predictedDiacritics != 0:
    precision = 100*correctDiacritics/predictedDiacritics
  recall = 100*correctDiacritics/totalDiacritics
  return (wla, precision, recall)

def restoreIdentity(dataset):
  return dataset['test']

def restoreUnigramsTraining(dataset):
  unigrams = dict()
  for trainSent in dataset['train']:
    for t in word_tokenize(trainSent):
      asciiToken = stripDiacritics(t)
      if not asciiToken in unigrams:
        unigrams[asciiToken] = dict()
      unigrams[asciiToken][t] = unigrams[asciiToken].get(t,0) + 1
  ans = dict()
  for k in unigrams:
    bestCount = 0
    for cand in unigrams[k]:
      if unigrams[k][cand] > bestCount:
        ans[k] = cand
        bestCount = unigrams[k][cand]
  return ans

def restoreUnigrams(dataset):
  pickleFile = 'models/unigram-'+dataset['slug']+'.pickle'
  if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as handle:
      bestRestoration = pickle.load(handle)
  else:
    bestRestoration = restoreUnigramsTraining(dataset)
    with open(pickleFile, 'wb') as handle:
      pickle.dump(bestRestoration, handle, protocol=pickle.HIGHEST_PROTOCOL)
  ans = []
  for strippedSent in dataset['test']:
    restoredString = ''
    lastIndex = 0
    for start, end in NLTKWordTokenizer().span_tokenize(strippedSent):
      restoredString += strippedSent[lastIndex:start]
      asciiToken = strippedSent[start:end]
      restoredString += bestRestoration.get(asciiToken, asciiToken)
      lastIndex = end
    restoredString += strippedSent[lastIndex:]
    ans.append(restoredString)
  return ans

# Returns a dict with benchmark names as keys and dicts as values
# Keys of those dicts are the algorithms names, values are numerical tuples
def evaluateAll(benchmarks, algorithms, dataDir):
  ans = dict()
  for benchmark in benchmarks:
    ans[benchmark] = dict()
    dataset = retrieveDataset(benchmark, dataDir)
    testCorpus = dataset['test']
    dataset['test'] = list(map(stripDiacritics, testCorpus))
    # writeCorpusToFile(dataset['test'], benchmark+'-ascii.txt')
    for k in algorithms:
      outputFile = 'predictions/'+benchmark+'-'+slugify(k)+'.txt'
      if os.path.exists(outputFile):
        predictions = readCorpusFromFile(outputFile)
      else:
        predictions = algorithms[k](dataset)
        writeCorpusToFile(predictions, outputFile)
      ans[benchmark][k] = score(predictions, testCorpus)
  return ans

def printMarkdown(allResults):
  if (len(allResults.keys())==1):
    print('There is currently **1** benchmark for this task.')
  else:
    countStr = '**'+str(len(allResults))+'**'
    print('There are currently', countStr, 'benchmarks for this task.')

  for benchmark in allResults:
    print("\n##",benchmark,'([README](../../datasets/'+benchmark+'/README.md))')
    metrics = ('WLA','Precision','Recall')
    print('|Algorithm|'+('|'.join(metrics))+'|')
    print('|---|'+('---|'*len(metrics)))
    resultHash = allResults[benchmark]
    for p in sorted(resultHash.items(), key=lambda x: x[1][0], reverse=True):
      print('|'+p[0]+'|'+('|'.join(map(lambda x: '{:.2f}'.format(x),p[1])))+'|')

def main():
  benchmarks = ('tuairisc', 'charles')
  algorithms = {
    'Keep as ASCII': restoreIdentity,
    'Unigrams': restoreUnigrams,
  }
  dataDir='datasets/'
  mkdir_p(dataDir)
  mkdir_p('models')
  mkdir_p('predictions')
  printMarkdown(evaluateAll(benchmarks, algorithms, dataDir))

main()
