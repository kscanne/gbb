
**Name**: TwittIrish UD Treebank

**Description**: “The TwittIrish treebank contains 866 Irish language tweets from two corpora: 166 tweets from the Cassidy Twitter Corpus [CTC] and 700 tweets from the Lynn Twitter Corpus [LTC].

* CTC consists of 25000 tweets posted between 2010 and 2019 randomly sampled from a database of 14111 users who have tweeted in Irish.
* LTC consists of 1493 tweets posted between 2009 and 2014 randomly sampled from 950000 tweets by 8000 users. Lemmas and POS-tags were added to LTC a part of a PhD research project by Dr. Teresa Lynn at Dublin City University, Ireland...

Trees were parsed automatically using the Irish UD Treebank (IUDT) (Lynn and Foster, 2016) as training data, followed by manual review.”

A full description is available
[here](https://github.com/UniversalDependencies/UD_Irish-TwittIrish/blob/master/README.md).

**Version**: UD version 2.10 (2022-05-15)

**Home page**: <https://universaldependencies.org/treebanks/ga_twittirish/index.html>

**Direct download**: <https://github.com/UniversalDependencies/UD_Irish-TwittIrish/archive/refs/heads/master.zip>

**Preview**:
~~~
# sent_id = 1003710197318275072
# text = RT @tuairiscnuacht: Corn an Aire tugtha leo ag fir na Mí, @wolfetonesmeath. Comghairdeachas leo. Is í seo an chéad uair go bhfuil craobh na…
1	RT	rt	SYM	_	_	4	parataxis:rt	_	_
2	@tuairiscnuacht	@tuairiscnuacht	PROPN	_	_	4	vocative:mention	_	SpaceAfter=No
3	:	:	PUNCT	_	_	4	punct	_	_
4	Corn	corn	PROPN	_	_	0	root	_	Lang=ga
5	an	an	DET	_	_	6	det	_	Lang=ga
6	Aire	aire	PROPN	_	_	4	nmod	_	Lang=ga
7	tugtha	tugtha	ADJ	_	_	4	xcomp:pred	_	Lang=ga
8	leo	le	ADP	_	_	7	obl:prep	_	Lang=ga
~~~

**BibTeX**:
~~~
@misc{iudt,
    author = "Cassidy, Lauren and Lynn, Teresa and Foster, Jennifer and McGuinness, Sarah",
    title = "The TwittIrish Universal Dependencies Treebank",
    publisher = "Universal Dependencies project",
    edition = "UD 2.10",
    year = "2022",
    url = {https://github.com/UniversalDependencies/UD_Irish-TwittIrish} }
~~~
