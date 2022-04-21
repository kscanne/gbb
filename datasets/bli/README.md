
**Name**: Corpus for Scottish Gaelic-Irish bilingual lexicon induction

**Description**: This dataset is a collection of 40000
Scottish Gaelic-Irish word pairs derived from the lexicon that underlies
the [Intergaelic machine translation engine](http://www.intergaelic.com/gd-ga/trans/).
All words have been lowercased.
We restricted to pairs where the word on each side was among
the top 50000 most frequent words in a fixed reference corpus.
The pairs are unique, but individual words (both source and target) 
sometimes appear multiple times when many translations are possible,
or because of mutation differences between source and target.
The pairs were randomized and then split into 
training (30000 pairs), development (5000 pairs), and test (5000 pairs)
sets.

**License**: GNU GPL v3.0. See <https://github.com/kscanne/caighdean/blob/master/LICENSE>

**Version**: 2022-04-21

**Home page**: <https://github.com/kscanne/gbb/tree/main/datasets/bli>

**Direct download**: <https://cs.slu.edu/~scannell/gbb/bli-gd-ga.zip>

**Preview**:
~~~
uirsgeul finscéal
comhdhail gcomhdháil
canaanaich canánaigh
tiormachd triomach
deargannan dreancaidí
pòlainn polainne
t-sligh' tslí
sheargadh seargadh
cho-theagsa chomhthéacs
t-ath-sgrùdadh t-athbhreithniú
~~~

**BibTeX**:
~~~
@misc{bli,
 title = {Corpus for Scottish Gaelic-Irish bilingual lexicon induction},
 author = {Scannell, Kevin},
 url = {https://github.com/kscanne/gbb/tree/main/datasets/bli},
 year = {2022} }
~~~
