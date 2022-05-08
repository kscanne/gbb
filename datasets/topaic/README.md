
**Name**: Corpus of Irish new articles with category labels

**Description**: This is a corpus of 2200 news articles from the online Irish news service Tuairisc.ie, in which each article is annotated with one of the following 11 categories:

|---|---|
|cultur-litriocht|Culture: Literature|
|cultur-scannan|Culture: Film|
|cultur-teilifis-raidio|Culture: TV/Radio|
|nuacht-gaeltacht|News: Gaeltacht|
|nuacht-idirnaisiunta|News: International|
|nuacht-naisiunta|News: National|
|pobal|Community|
|sport-cluichi-gaelacha|Sport: Gaelic Games|
|sport-rugbai|Sport: Rugby|
|sport-sacar|Sport: Soccer|
|tuairimiocht|OpEd|

These categories are taken from the structure of the tuairisc.ie website 
itself. For simplicity, we have only selected articles which appear
in a single category for this corpus.

The corpus contains 200 articles from each category,
which have been split into training (80%), development (10%),
and test sets (10%).
We followed the convention established by the
[Tuairisc.ie corpus](https://github.com/kscanne/gbb/tree/main/datasets/tuairisc)
by only using files published in 2015 for the development and test sets.
Anyone making use of a pre-trained language model with this dataset
should ensure that articles from Tuairisc.ie published in 2015 
are omitted from their model.

The articles were downloaded from the Tuairisc.ie website, and care was taken to remove boilerplate text, ads, and so on. In all, the corpus contains about
1.3 million words across the 2200 articles.

All articles are Copyright 2014–2022 Tuairisc Bheo Teoranta.

**Version**: 2022-05-08

**Home page**: <https://github.com/kscanne/gbb/tree/main/datasets/topaic>

**Direct download**: <https://cs.slu.edu/~scannell/gbb/topaic.zip>

**Preview**:
~~~
train/cultur-litriocht/000.txt:

Reáchtálfar comhdháil lae i gColáiste Mhuire gan Smál i Luimneach
inniu in ómós don údar Gaeilge aitheanta, Pádraic Breathnach.

Pléifidh an chomhdháil, atá á heagrú ag Roinn na Gaeilge sa
choláiste inar chaith Breathnach féin an chuid is mó dá shaol oibre
mar léachtóir, le téamaí agus gnéithe éagsúla dá ghearrscéalta
agus úrscéalta.

Tá an chomhdháil á heagrú chun ceiliúradh a dhéanamh ar an
scríbhneoir aitheanta, a bhfuil duaiseanna litríochta go leor bronnta
~~~

**BibTeX**:
~~~
@misc{topaic,
 title = {Irish new categorization corpus},
 author = {Scannell, Kevin},
 url = {https://github.com/kscanne/gbb/tree/main/datasets/topaic},
 copyright = {Copyright 2014-2022, Tuairisc Bheo Teoranta},
 year = {2022} }
~~~
