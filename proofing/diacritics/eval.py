import os.path
import urllib.request
import ssl
import zipfile
import lzma
import pickle
import diacritization_stripping_data
from nltk.tokenize import word_tokenize, NLTKWordTokenizer

def stripDiacritics(s):
  m = diacritization_stripping_data.strip_diacritization_uninames
  return ''.join(map(lambda c: m.get(c,c), s))

def hasDiacritics(s):
  m = diacritization_stripping_data.strip_diacritization_uninames
  return any(c in m for c in s)

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

def retrieveDataset(name):
  ans = dict()
  files = ('dev','test','train')
  if name == 'Tuairisc 2015':
    if not all(os.path.exists(x+'-clean.txt') for x in files):
      zipfileName = 'tuairisc-2015.zip'
      if not os.path.exists(zipfileName):
        zipURL = 'https://cs.slu.edu/~scannell/gbb/'+zipfileName
        urlRetrieveNoSSL(zipURL, zipfileName)
      with zipfile.ZipFile(zipfileName, 'r') as zipRef:
        zipRef.extractall()
    for x in files:
      ans[x] = readCorpusFromFile(x+'-clean.txt')
    ans['shortName'] = 'tuairisc'
  elif name == 'Charles University':
    if not all(os.path.exists('ga/target_'+x+'.txt.xz') for x in files):
      zipfileName = 'ga.zip'
      if not os.path.exists(zipfileName):
        zipURL = 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2607/ga.zip?sequence=1&isAllowed=y'
        urllib.request.urlretrieve(zipURL, zipfileName)
      with zipfile.ZipFile(zipfileName, 'r') as zipRef:
        zipRef.extractall()
    for x in files:
      ans[x] = readCorpusFromXZFile('ga/target_'+x+'.txt.xz')
    ans['shortName'] = 'charles'
  else:
    sys.exit("Unknown dataset\n")
  return ans

# returns a tuple: (WER, Precision, Recall)
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
      
  wer = correctWords/totalWords
  precision = float('nan')
  if predictedDiacritics != 0:
    precision = correctDiacritics/predictedDiacritics
  recall = correctDiacritics/totalDiacritics
  return (wer, precision, recall)

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
  pickleFile = 'unigram-'+dataset['shortName']+'.pickle'
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
def evaluateAll(benchmarks, algorithms):
  ans = dict()
  for benchmark in benchmarks:
    ans[benchmark] = dict()
    dataset = retrieveDataset(benchmark)
    testCorpus = dataset['test']
    dataset['test'] = list(map(stripDiacritics, testCorpus))
    for k in algorithms:
      predictions = algorithms[k](dataset)
      ans[benchmark][k] = score(predictions, testCorpus)
  return ans

def decFormat(x):
  return '{:.3f}'.format(x)

def printMarkdown(allResults):
  print("## Diacritic Restoration\n")
  if (len(allResults.keys())==1):
    print('There is currently **1** benchmark for this task.')
  else:
    countStr = '**'+str(len(allResults))+'**'
    print('There are currently', countStr, 'benchmarks for this task.')

  for benchmarkName in allResults:
    print("\n##",benchmarkName)
    metrics = ('WER','Precision','Recall')
    print('|Algorithm|'+('|'.join(metrics))+'|')
    print('|---|'+('---|'*len(metrics)))
    resultHash = allResults[benchmarkName]
    for p in sorted(resultHash.items(), key=lambda x: x[1][0], reverse=True):
      print('|'+p[0]+'|'+('|'.join(map(decFormat,p[1])))+'|')

def main():
  benchmarks = (
    'Tuairisc 2015',
    'Charles University',
  )
  algorithms = {
    'Keep as ASCII': restoreIdentity,
    'Unigrams': restoreUnigrams,
  }
  printMarkdown(evaluateAll(benchmarks, algorithms))

main()
