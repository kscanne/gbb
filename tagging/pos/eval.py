import os
import urllib.request
import ssl
import zipfile
import pickle
import re
import sys
import nltk

def mkdir_p(dir):
  if not os.path.exists(dir):
    os.makedirs(dir)

def slugify(name):
  return re.sub('[^A-Za-z]', '', name)

def writeCorpusToTwoCols(corpus, fileName):
  with open(fileName, "w", encoding="utf-8") as f:
    for sent in corpus:
      for taggedtok in sent:
        f.write('\t'.join(taggedtok)+'\n')
      f.write('\n')

def readCorpusFromTwoCols(fileName):
  with open(fileName, "r", encoding="utf-8") as f:
    ans = []
    currsent = []
    for line in f:
      line = line.rstrip()
      if len(line)==0:
        if len(currsent)>0:
          ans.append(currsent)
          currsent = []
      else:
        currsent.append(tuple(line.split('\t')))
  return ans

def readDictFromTwoCols(fileName):
  with open(fileName, "r", encoding="utf-8") as f:
    ans = [tuple(line.rstrip().split('\t')) for line in f]
  return ans

def hasFeature(fdict, key, val=None):
  if val==None:
    return key in fdict
  else:
    return key in fdict and fdict[key]==val

def featureDict2Parole(fdict, slotlist):
  ans = ''
  toParole = {'NomAcc': 'c', 'Imp': 'm', 'Past': 's', 'Num': 'm'}
  for slot in slotlist:
    if slot in fdict:
      if slot=='Tense':
        if hasFeature(fdict, 'Aspect', 'Imp'):
          ans += 'h'
          continue
        if hasFeature(fdict, 'Aspect', 'Hab'):
          ans += 'g'
          continue
      val = fdict[slot]
      if val in toParole:
        ans += toParole[val]
      else:
        ans += val[0].lower()
    else:
      ans += '-'
  ans = re.sub('-+$', '', ans)
  return ans

# pass UD data and return PAROLE tag (best effort)
def generateFullTag(lemma, upos, featstr):
  featdict = dict()
  if '=' in featstr:
    for piece in featstr.split('|'):
      k,v = piece.split('=')
      featdict[k] = v
  basetag = {'ADJ': 'Aq', 'ADP': 'Sp', 'ADV': 'R', 'AUX': 'W', 'CCONJ': 'Cc', 'DET': 'D', 'INTJ': 'I', 'NOUN': 'Nc', 'NUM': 'M', 'PART': 'U', 'PRON': 'P', 'PROPN': 'Np', 'PUNCT': 'Fp', 'SCONJ': 'Cs', 'SYM': 'Xs', 'VERB': 'Vm', 'X': 'X'}
  ans = basetag[upos]
  if upos=='ADJ':
    if hasFeature(featdict, 'VerbForm', 'Part'):
      ans = 'Av'
    else:
      ans += featureDict2Parole(featdict,['Degree', 'Gender', 'Number', 'Case'])
  elif upos=='ADP':
    if hasFeature(featdict, 'PronType', 'Art'):  # before next!
      ans += 'a'
      ans += featureDict2Parole(featdict,['Gender', 'Number']) # Gender == -
    elif hasFeature(featdict, 'Number'):  # agam, etc.
      ans = 'Pr'
      ans += featureDict2Parole(featdict,['Person', 'Gender', 'Number'])
    elif hasFeature(featdict, 'PrepForm', 'Cmpd'):
      ans += 'c'
    elif hasFeature(featdict, 'Poss'):
      ans += 'p'
      if hasFeature(featdict, 'Number'):
        ans += '-'
        ans += featureDict2Parole(featdict,['Number']) 
  #  handle upos=='ADV"... map to Rg, Rd, Ri, etc.?
  elif upos=='AUX':
    if hasFeature(featdict,'Tense','Past') or hasFeature(featdict,'Mood','Cnd'):
      ans += 's'
    else:
      ans += 'p'
    if hasFeature(featdict, 'PronType', 'Rel'):
      ans += 'r'   # UD doesn't currently distinguish indirect ('s' in PAROLE)
    else:
      ans += '-'
    if hasFeature(featdict, 'Mood', 'Int'):
      ans += 'q'
    else:
      ans += 'i'
    if hasFeature(featdict, 'Polarity', 'Neg'):
      ans += 'n'
  elif upos=='DET':
    if hasFeature(featdict, 'PronType', 'Art'):
      ans = 'Td-'
      # Gender first in Elaine's thesis, but never specified in her corpus
      ans += featureDict2Parole(featdict,['Number', 'Case'])
    elif hasFeature(featdict, 'PronType', 'Dem'):
      ans = 'Dd'
    elif hasFeature(featdict, 'PronType', 'Ind'):
      ans = 'Di'
    elif hasFeature(featdict, 'Poss'):
      ans = 'Dp'
      ans += featureDict2Parole(featdict,['Person', 'Gender', 'Number'])
    elif hasFeature(featdict, 'Definite', 'Def'):
      ans = 'Dq'
    # interrogative determiners?  Dw
  elif upos=='NOUN':
    if hasFeature(featdict, 'VerbForm'):
      ans = 'Nv'
      if hasFeature(featdict, 'Case', 'Gen'):
        ans += '--g'
    elif not hasFeature(featdict, 'Gender'):
      ans = 'Ns'
      if hasFeature(featdict, 'Number', 'Sing'):
        ans += '-s'
    else:
      ans += featureDict2Parole(featdict, ['Gender', 'Number', 'Case'])
      if hasFeature(featdict, 'Emp'):
        ans += '-e'
  elif upos=='NUM':
    if re.match('^[IVXLCDM]+$', lemma):
      ans = 'Mr'
    elif re.match('^[0-9]+$', lemma):
      ans = 'Mn'
    elif hasFeature(featdict, 'NumType', 'Card'):
      ans = 'Mc'
    elif hasFeature(featdict, 'NumType', 'Ord'):
      ans = 'Mo'
  elif upos=='PART':
    if hasFeature(featdict, 'PartType', 'Vb'):
      ans = 'Q'
      if hasFeature(featdict, 'Polarity', 'Neg'):
        ans += 'n'
    elif hasFeature(featdict, 'Form', 'Indirect'):  # lenar, ina, faoina, etc.
      ans = 'Spr'
    elif hasFeature(featdict, 'PartType', 'Inf'):
      ans = 'Sp'  # "a dhéanamh"
    elif hasFeature(featdict, 'PartType', 'Cop'):
      pass  # 1x in UD
    elif hasFeature(featdict, 'PartType', 'Cmpl'):
      pass  # Fix?
    else:  # Ua, Up, Uc, Us, Uv, Um, Ud
      ans += featureDict2Parole(featdict, ['PartType'])
  elif upos=='PRON':
    if hasFeature(featdict, 'Reflex', 'Yes'):
      ans = 'Px'
    elif hasFeature(featdict, 'PronType', 'Ind'):
      ans = 'Pi'
    elif hasFeature(featdict, 'PronType', 'Dem'):
      ans = 'Pd'
    else:
      ans = 'Pp'
      ans += featureDict2Parole(featdict, ['Person', 'Gender', 'Number'])
      if lemma in ['sé', 'siad', 'sí']:
        ans += 's'
  elif upos=='PROPN':
    ans += featureDict2Parole(featdict, ['Gender', 'Number', 'Case'])
  elif upos=='SCONJ':
    if hasFeature(featdict, 'VerbForm', 'Cop'):
      ans += 'w'  # Csw
    else:
      ans += '-'
    if hasFeature(featdict, 'Tense', 'Past'):
      ans += 's'  # e.g. sular/Cs-s fhág...
    ans = re.sub('-$', '', ans)
  elif upos=='VERB':
    ans += featureDict2Parole(featdict, ['Mood', 'Tense', 'Person', 'Number'])
  elif upos=='X':
    if hasFeature(featdict, 'Foreign', 'Yes'):
      ans += 'f'
    else:
      ans += 'x'
  # Sort out Punct somehow based on lemma?
  # Fa=quote initial, Fb=hyphen, Fe=sentence final, Fi=sentence internal
  # Fp=other, Fz=quote final
  if hasFeature(featdict, 'Abbr'):
    ans = 'Y'
  return ans

# if second arg is True, convert features into extended POS tags
def readCorpusFromCoNNL_U(fileName, full_p):
  with open(fileName, "r", encoding="utf-8") as f:
    ans = []
    currsent = []
    for line in f:
      line = line.rstrip()
      if len(line)==0:
        if len(currsent)>0:
          ans.append(currsent)
          currsent = []
      elif line[0]=='#':
        pass
      else:
        pieces = line.split('\t')
        if full_p:
          fullTag = generateFullTag(pieces[2],pieces[3],pieces[5])
          currsent.append((pieces[1], fullTag))
        else:
          currsent.append((pieces[1], pieces[3]))
  return ans

def writeTagDict(tagDict, fileName):
  with open(fileName, "w", encoding="utf-8") as f:
    for taggedWord in tagDict:
      f.write('\t'.join(taggedWord)+'\n')

def readTagDict(fileName, full_p):
  ans = []
  with open(fileName, "r", encoding="utf-8") as f:
    for line in f:
      pieces = line.rstrip().split('\t')
      if full_p:
        fullTag = generateFullTag(pieces[1],pieces[2],pieces[4])
        ans.append((pieces[0], fullTag))
      else:
        ans.append((pieces[0], pieces[2]))
  return ans

# because SLU systems are awful
def urlRetrieveNoSSL(url, fileName):
  with urllib.request.urlopen(url, context=ssl.SSLContext()) as u, \
                        open(fileName, 'wb') as f:
    f.write(u.read())

def retrieveZip(url, zipName, dest):
  pathToZip = dest+'/'+zipName
  if not os.path.exists(pathToZip):
    urlRetrieveNoSSL(url, pathToZip)
  with zipfile.ZipFile(pathToZip, 'r') as zipRef:
    zipRef.extractall(path=dest)

def retrieveTagDict(name):
  dest = 'datasets'
  fileName = dest+'/'+name+'-dict.tsv'
  if not os.path.exists(fileName):
    if not os.path.exists(dest+'/tagdict.tsv'):
      zipfileName = 'tagdict.zip'
      zipURL = 'https://cs.slu.edu/~scannell/gbb/'+zipfileName
      retrieveZip(zipURL, zipfileName, dest)
    pairs = readTagDict(dest+'/tagdict.tsv', '-full' in name)
    writeTagDict(pairs, fileName)
  else:
    pairs = readDictFromTwoCols(fileName)
  return pairs

def retrieveDataset(name):
  retrieveTagDict(name)
  dest = 'datasets'
  ans = {'slug' : name}
  files = ('dev','test','train')
  if name[:4] == 'iudt':
    if not all(os.path.exists(dest+'/'+name+'-'+x+'.tsv') for x in files):
      zipfileName = 'master.zip'
      zipURL = 'https://github.com/UniversalDependencies/UD_Irish-IDT/archive/refs/heads/'+zipfileName
      retrieveZip(zipURL, zipfileName, dest)
    for x in files:
      ans[x] = readCorpusFromCoNNL_U(dest+'/UD_Irish-IDT-master/ga_idt-ud-'+x+'.conllu', '-full' in name)
      writeCorpusToTwoCols(ans[x], dest+'/'+name+'-'+x+'.tsv')
  else:
    sys.exit('Unknown dataset: '+name+'\n')
  return ans

def stripTags(sent):
  return [p[0] for p in sent]

# returns a 1-tuple: (Accuracy)
def score(predictedCorpus, goldCorpus):
  totalWords = 0
  correctWords = 0
  for predictedSent, goldSent in zip(predictedCorpus, goldCorpus):
    for ptok, gtok in zip(predictedSent, goldSent):
      totalWords += 1
      if ptok[1] == gtok[1]:
        correctWords += 1
  return (100*correctWords/totalWords,)

# returns dict of tag counts in train
def getTagCountsTraining(dataset):
  pickleFile = 'models/tagFreqs-'+dataset['slug']+'.pickle'
  if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as handle:
      ans = pickle.load(handle)
  else:
    ans = dict()
    for sent in dataset['train']:
      for taggedtok in sent:
        ans[taggedtok[1]] = 1 + ans.get(taggedtok[1],0)
    with open(pickleFile, 'wb') as handle:
      pickle.dump(ans, handle, protocol=pickle.HIGHEST_PROTOCOL)
  return ans

def bestSingleTag(dataset):
  tagCounts = getTagCountsTraining(dataset)
  mostFrequentTag = max(tagCounts, key=tagCounts.get)
  ans = []
  for sent in dataset['test']:
    outputsent = []
    for taggedtok in sent:
      outputsent.append((taggedtok[0],mostFrequentTag))
    ans.append(outputsent)
  return ans

def buildNLTKRegexTagger(dataset):
  tagCounts = getTagCountsTraining(dataset)
  mostFrequentTag = max(tagCounts, key=tagCounts.get)
  if '-full' in dataset['slug']:
    pattFile = 'suffix-full.tsv'
    properTag = 'Npms'
  else:
    pattFile = 'suffix.tsv'
    properTag = 'PROPN'
  patterns = []
  with open(pattFile, "r", encoding="utf-8") as f:
    for line in f:
      pieces = line.rstrip().split('\t')
      patterns.append(('.*'+pieces[0]+'$', pieces[1]))
  patterns.append((r'.*[A-ZÁÉÍÓÚ].*', properTag))
  patterns.append((r'.*', mostFrequentTag))
  return nltk.RegexpTagger(patterns)

def buildNLTKUnigramTagger(dataset):
  tagCounts = getTagCountsTraining(dataset)
  mostFrequentTag = max(tagCounts, key=tagCounts.get)
  #badTagger = nltk.DefaultTagger(mostFrequentTag)
  defaultTagger = buildNLTKRegexTagger(dataset)
  return nltk.UnigramTagger(dataset['train'], backoff=defaultTagger)

def unigramTagger(dataset):
  pickleFile = 'models/'+dataset['slug']+'-unigram.pickle'
  if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as handle:
      unigramModel = pickle.load(handle)
  else:
    unigramModel = buildNLTKUnigramTagger(dataset)
    with open(pickleFile, 'wb') as handle:
      pickle.dump(unigramModel, handle, protocol=pickle.HIGHEST_PROTOCOL)
  testNoTags = [stripTags(s) for s in dataset['test']]
  return unigramModel.tag_sents(testNoTags)

def buildNLTKBigramTagger(dataset):
  unigramModel = buildNLTKUnigramTagger(dataset)
  return nltk.BigramTagger(dataset['train'], backoff=unigramModel)

def bigramTagger(dataset):
  pickleFile = 'models/'+dataset['slug']+'-bigram.pickle'
  if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as handle:
      bigramModel = pickle.load(handle)
  else:
    bigramModel = buildNLTKBigramTagger(dataset)
    with open(pickleFile, 'wb') as handle:
      pickle.dump(bigramModel, handle, protocol=pickle.HIGHEST_PROTOCOL)
  testNoTags = [stripTags(s) for s in dataset['test']]
  return bigramModel.tag_sents(testNoTags)

def trigramTagger(dataset):
  pickleFile = 'models/'+dataset['slug']+'-trigram.pickle'
  if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as handle:
      trigramModel = pickle.load(handle)
  else:
    bigramModel = buildNLTKBigramTagger(dataset)
    trigramModel = nltk.TrigramTagger(dataset['train'], backoff=bigramModel)
    with open(pickleFile, 'wb') as handle:
      pickle.dump(trigramModel, handle, protocol=pickle.HIGHEST_PROTOCOL)
  testNoTags = [stripTags(s) for s in dataset['test']]
  return trigramModel.tag_sents(testNoTags)

def hmmTagger(dataset):
  pickleFile = 'models/'+dataset['slug']+'-hmm.pickle'
  if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as handle:
      hmmModel = pickle.load(handle)
  else:
    hmmModel = nltk.HiddenMarkovModelTagger.train(dataset['train'])
    #with open(pickleFile, 'wb') as handle:
    #  pickle.dump(hmmModel, handle, protocol=pickle.HIGHEST_PROTOCOL)
  testNoTags = [stripTags(s) for s in dataset['test']]
  return hmmModel.tag_sents(testNoTags)

def perceptronTagger(dataset):
  pickleFile = 'models/'+dataset['slug']+'-perceptron.pickle'
  if os.path.exists(pickleFile):
    with open(pickleFile, 'rb') as handle:
      pModel = pickle.load(handle)
  else:
    pModel = nltk.tag.perceptron.PerceptronTagger(load=False)
    pModel.train(dataset['train'])
    with open(pickleFile, 'wb') as handle:
      pickle.dump(pModel, handle, protocol=pickle.HIGHEST_PROTOCOL)
  testNoTags = [stripTags(s) for s in dataset['test']]
  return pModel.tag_sents(testNoTags)

def crfTagger(dataset):
  crfModel = nltk.tag.CRFTagger()
  modelFile = 'models/'+dataset['slug']+'.crf.tagger'
  if os.path.exists(modelFile):
    crfModel.set_model_file(modelFile)
  else:
    crfModel.train(dataset['train'], modelFile)
  testNoTags = [stripTags(s) for s in dataset['test']]
  return crfModel.tag_sents(testNoTags)

# Returns a dict with benchmark names as keys and dicts as values
# Keys of those dicts are the algorithms names, values are numerical tuples
def evaluateAll(benchmarks, algorithms):
  ans = dict()
  for benchmark in benchmarks:
    sys.stderr.write('Benchmark: '+benchmark+'\n')
    ans[benchmark] = dict()
    dataset = retrieveDataset(benchmark)
    for k in algorithms:
      sys.stderr.write('  Algorithm: '+k+'\n')
      outputFile = 'predictions/'+benchmark+'-'+slugify(k)+'.tsv'
      if os.path.exists(outputFile):
        predictions = readCorpusFromTwoCols(outputFile)
      else:
        predictions = algorithms[k](dataset)
        writeCorpusToTwoCols(predictions, outputFile)
      ans[benchmark][k] = score(predictions, dataset['test'])
  return ans

# benchmarks is passed to preserve the preferred order in the README
def printMarkdown(benchmarks, allResults):
  if (len(benchmarks)==1):
    print('There is currently **1** benchmark for this task.')
  else:
    countStr = '**'+str(len(benchmarks))+'**'
    print('There are currently', countStr, 'benchmarks for this task.')

  for benchmark in benchmarks:
    dirname = benchmark
    fullpos = dirname.find('-full')
    if fullpos != -1:
      dirname = dirname[:fullpos]
    print("\n##",benchmark,'([README](../../datasets/'+dirname+'/README.md))')
    metrics = ('Accuracy',)
    print('|Algorithm|'+('|'.join(metrics))+'|')
    print('|---|'+('---|'*len(metrics)))
    for p in sorted(allResults[benchmark].items(), key=lambda x: x[1][0], reverse=True):
      print('|'+p[0]+'|'+('|'.join(map(lambda x: '{:.2f}'.format(x),p[1])))+'|')

def main():
  # twittirish is test only for now
  benchmarks = ('iudt', 'iudt-full')
  algorithms = {
    'Best single tag': bestSingleTag,
    'Unigram tagger': unigramTagger,
    'Bigram tagger': bigramTagger,
    'Trigram tagger': trigramTagger,
    'HMM tagger': hmmTagger,
    'Perceptron': perceptronTagger,
    'CRF tagger': crfTagger,
  }
  mkdir_p('datasets')
  mkdir_p('models')
  mkdir_p('predictions')
  printMarkdown(benchmarks, evaluateAll(benchmarks, algorithms))

main()
