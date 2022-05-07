
**Name**: Irish Twitter corpus labeled by sentiment

**Description**: This is a corpus of 24000 Irish language tweets posted to Twitter between 2007 and 2022. There are about 360k words across the 24000 tweets in the corpus. Tweets with positive sentiment are labeled with +1, and those with negative sentiment are labeled -1.

Instead of manually annotating, we used the presence of certain
emoji/emoticons as a proxy for sentiment.
We fixed the following set of positive emoji:
~~~
😀😂😃😄😛😅😆😎😇😁😊👍🙂😋😌😍
~~~
and the set of positive emoticons as those matching this regular expression:
~~~
[:;=8][o^-]?[})D>]
~~~

The following is the set of negative emoji:
~~~
😞😟😠😡😕🙁😣😔😖😫👎😩😤😮😱😨😰😦😧😢😥😪😓😒
~~~
and the set of positive emoticons as those matching this regular expression:
~~~
[:;=8][o^-]?[(<{]
~~~

The positive label (+1) was then assigned to any tweet which
contained at least one positive emoji or emoticon and no negative ones.
The negative label (-1) was assigned to any tweet which contained
at least one negative emoji or emoticon and no positive ones.
All emojis/emoticons were then removed from the tweets in the dataset
(otherwise the classification task would be trivial).

We started with the full set of Irish language tweets as
identified by the website [Indigenous Tweets](http://indigenoustweets.com/ga/),
filtered out retweets, and then labeled the remaining tweets using
the scheme above. The dataset was then assembled by taking a
random sample of 12000 tweets labeled +1 and 12000 tweets labeled -1.
It's worth nothing that there are many more tweets labeled +1 then -1 in
the full Indigenous Tweets collection, and we've artificially
forced the label priors to be 50/50 to make the classification task
more challenging.

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
Embedded tabs or newlines were replaced with spaces, so each tweet 
appears on a single line in the corpus, for convenience while processing.

Copyright remains with the original authors of the tweets.
All rights reserved.

**Version**: 2022-05-07

**Home page**: <https://github.com/kscanne/gbb/tree/main/datasets/sentiment>

**Direct download**: <https://cs.slu.edu/~scannell/gbb/sentiment.zip>

**Preview**:
~~~
1	<USER> comhghairdeachas ar shraith iontach!! Ag súil go mór leis an gcéad ceann eile
-1	Faoi Roinn Cluiche Leath Cheannais mins nd half Gaoth Dobhair : ( ) Naomh Conaill : )
-1	Sin deireadh lenár samhradh
1	<USER> <USER> <USER> <USER> <USER> Suíomh íontach é seo Go breá teacht ar an litriú ceart do Mc Breen freisin Níl morán dúinn ann ach táimid láidir in oirthear an Cábháin ar a laghad! EastCavan <URL>
1	<USER> is fearr Gaeilge briste ná Béarla cliste
-1	Ba breá liom dul chuig an Cabaret Craiceáilte ar an sathairn seo ach ní thig liom brónach
1	Ar fheabhas! <URL>
1	<USER> <USER> <USER> Sure níl a dhath ar bith folláin ar an aimsir seo!
1	<USER> <USER> An rud is tábhachtaí ar fad
1	<USER> <USER> <USER> Caith súil ar a scríobhann tú i gcónaí
~~~

**BibTeX**:
~~~
@misc{sentiment-ga,
 title = {Irish Twitter corpus labeled by sentiment},
 author = {Scannell, Kevin},
 url = {https://github.com/kscanne/gbb/tree/main/datasets/sentiment},
 copyright = {Copyright 2007-2022, All Rights Reserved},
 year = {2022} }
~~~
