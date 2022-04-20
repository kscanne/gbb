
**Name**: Tuairisc.ie 2015 corpus

**Description**: This is a corpus of articles published by the Irish language online news service Tuairisc.ie in 2015. The corpus consists of just over 1.5 million words of text, segmented into sentences, and split into training, development, and test sets (80%-10%-10%). The articles were downloaded from the Tuairisc.ie website, and care was taken to remove boilerplate text, ads, and so on. All URLs, email addresses, and Twitter-style usernames were replaced with special tokens (`<URL>`, `<EMAIL>`, `<USER>`). 

We aim to establish this corpus as a standard test set for a number
of natural language processing tasks.  By setting aside articles from
the calendar year 2015, we hope it will be easier for researchers
to create large pre-trained language models that leave out these
texts in order to give fair evaluations.

This corpus was originally designed for evaluating diacritic restoration systems, and so we invested a lot of effort in correcting errors involving diacritics in order to give the most realistic evaluations possible. Errors of this kind are extremely common in online Irish texts, even in well-edited texts like those on Tuairisc.ie. In all, we corrected **3642** words by either adding or removing diacritics.
We restricted these corrections to cases that were clearly errors (*ar **fail**, Seán **Ban** Breathnach*, **úafasach**), and left
examples that might represent a legitimate historical or dialect spelling unchanged. The *only* changes that were made to the original articles involved 
addition or removal of diacritics.  In particular, the number of Unicode characters in the corpus did not change as part of this cleaning process.

All articles are Copyright 2015 Tuairisc Bheo Teoranta.

**Version**: 2022-04-20

**Home page**: <https://github.com/kscanne/gbb/tree/main/datasets/tuairisc>

**Direct download**: <https://cs.slu.edu/~scannell/gbb/tuairisc-2015.zip>

**Preview**:

~~~
Céard atá amach romhainn sa tSraith Náisiúnta Peile, 2015?
Le teacht an earraigh, tá an tSraith Náisiúnta Peile á thosú arís an deireadh seachtaine seo, agus tar éis bhriseadh an gheimhridh, tá daoine ar fud na tíre ag feitheamh air arís.
Chun cabhrú linn súil a chaitheamh chun cinn ar céard atá le teacht sa tsraith, chuaigh Tuairisc.ie ar aistear chuig na ceithre chúige chun tuairimí daoine eolacha a fháil.
Céard iad a gcuid smaointe faoin shéasúr na bliana seo, mar sin?1.
Cé a bhuafaidh Roinn 1 den tSraith Náisiúnta Peile?
Baile Átha Cliath.
Is dóigh go mbeidh fonn orthu chuile chluiche i mbliana a bhuachan.
Scaoil siad leo Craobh na hÉireann anuraidh agus beidh siad ag iarraidh é sin a chur ina gceart.
Chonaic muid nach raibh aon Phlean B ag Gavin ach is dóigh gur fhoghlaim sé go leor uaidh sin.
Tá seans ann go bhfeicfidh muid cuid de na pleananna sin i rith na sraithe.
~~~

**BibTeX**:
~~~
@misc{tuairisc,
 title = {Tuairisc.ie 2015 corpus},
 author = {Scannell, Kevin},
 url = {https://github.com/kscanne/gbb/tree/main/datasets/tuairisc},
 copyright = {Copyright 2015 Tuairisc Bheo Teoranta, All Rights Reserved},
 year = {2015} }
~~~
