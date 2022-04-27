
**Name**: Twitter error corpus

**Description**: This is a corpus consisting of 5000
randomly sampled Irish language tweets 
in which all spelling and grammar errors have
been manually annotated. There are about 100000 tokens in all,
with over 3000 of these annotated with a correction of some kind.

The annotation scheme is based on what I call the
“confident Irish speaker” model.  This means that I've only corrected
what I believe to be spelling
or grammatical *errors*;
this is to say that intentional misspellings (*scéalllllll*,
*rev* for *raibh*), 
coinages (*creepáil*, *cacphostáil*),
accepted dialect spellings (*inniubh*, *dhuit*, *anso*, *goidé*),
and non-standard mutations (*ar an dtigh*, etc.) are **not**
treated as errors.
At the same time, we are targeting standard Irish spelling
as much as possible, and so we do correct some
non-standard forms, e.g. *tá'n* is corrected to *tá an*,
and *cungnamh* (acceptable in older texts) to *cúnamh*.
It's worth noting that these are edge cases; the 
vast majority of corrections are for obvious typos 
(often missing fadas) or simple grammatical errors (missing mutations, etc.).

The tweets have been tokenized, and the corpus files are provided
as tab-separated files with two columns.  The first column
contains the original tokens (after some pre-preprocessing,
described below), and the second column contains the corrected
tokens. The great majority of tokens are, of course, unchanged.
The token `\n` is used as a delimiter between tweets
(and nowhere else).

If a single token is corrected to multiple tokens, the correction
appears in the second column with a space:
~~~
Dá	Dá
mbeadh	mbeadh
ballaí	ballaí
theach	theach
tabhairne	tábhairne
Húdí	Húdaí
Bhig	Bhig
inann	in ann
labhairt	labhairt
~~~

If multiple tokens become a single token after correction,
the correction is aligned with the first token, and the 
second column is left blank for any tokens that follow:
~~~
Cairactéir	Carachtar
specialta	speisialta
,	,
sar	sáramhránaí
amhránaí	
.	.
~~~

We have introduced a new technique for splitting this corpus of tweets
into training, development, and test sets that is reproducible and which
will allow other researchers to build pre-trained models using Twitter
data while avoiding tweets in this test set in a disciplined way.
Namely, we compute the MD5 hash of the numeric tweet ID,
convert to hexadecimal, and extract the least significant hex digit.
If this digit is "e" or "f", the tweet is placed in the test set.
If this digit is "c" or "d", the tweet is placed in the development set,
and in all other cases, it is placed in the training set
(giving a 75%-12.5%-12.5% split).

Some gentle preprocessing was performed on the text of each tweet
to give some anonymity; Twitter usernames were replaced with
a special token `<USER>` and URLs were replaced with `<URL>`.

Copyright remains with the original authors of the tweets.
All rights reserved.

**Version**: 2022-04-27

**Home page**: <https://github.com/kscanne/gbb/tree/main/datasets/errors>

**Direct download**: <https://cs.slu.edu/~scannell/gbb/errors.zip>

**Preview**:
~~~
<USER>	<USER>
<USER>	<USER>
<USER>	<USER>
Comhghairdeas	Comhghairdeas
.	.
Là	Lá
iontach	iontach
a	a
bhi	bhí
ann	ann
.	.
\n	\n
Lón	Lón
deas	deas
i	i
~~~

**BibTeX**:
~~~
@misc{errors2022,
 title = {Corpus of Irish tweets with errors annotated},
 author = {Scannell, Kevin},
 url = {https://github.com/kscanne/gbb/tree/main/datasets/errors},
 year = {2022} }
~~~
