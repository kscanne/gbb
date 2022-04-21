
**Name**: Irish Twitter corpus labeled by Ó/Mac vs. Ní/Nic

**Description**: This is a corpus of 50000 Irish language tweets posted to Twitter between 2007 and 2022. There are about 800k words across the 50000 tweets in the corpus. We restricted to accounts whose (self-reported) name contains either "Ó", "Mac", "Ní", or "Nic". Tweets from users whose name contains "Ní" or "Nic" are labeled with a "0" in the dataset, and tweets from users whose name contains "Ó" or "Mac" are labeled with a "1".

To construct the corpus, we began with the top 50 "Ó/Mac" users and the top 50 "Ní/Nic" users as reported by the website [Indigenous Tweets](http://indigenoustweets.com/ga/). A random sample of 500 Irish tweets was chosen from each user after performing language identification and filtering out retweets.

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

**Version**: 2022-04-21

**Home page**: <https://github.com/kscanne/gbb/tree/main/datasets/inscne>

**Direct download**: <https://cs.slu.edu/~scannell/gbb/inscne.zip>

**Preview**:
~~~
0	<USER> <USER> is breá liom an format. Airím go bhfuilim san amharclann. Format an-spéisiúl
1	Article iontach maith San <USER> lch 56 faoi dornálaíocht amaitéarach na hÉireann <USER> <URL>
1	<USER> <USER> <USER> Ach déanfaidh cac maithe don talamh,nó an ndéanfaidh??
0	<USER> Is cuimhin mo mháthair ag inse an scéil sin domh. Alltacht ar fad a bhí orm!
0	Comhghairdeachas leat <USER> ar d’ainmniúchán mar ‘Pearsa Teilifíse na Bliana’ <USER> 👏🏼🤩 Láithreoir cumasach & bean chairdiúil álainn & nádúrtha. 💞✨💞 Cé go bhfuil an t-uafás oibre déanta agat le <USER>/<USER> bhí tú linne ar dtús <USER> 😜😅💜 <URL>
1	Grma le <USER> ó Thaillte an Choláiste agus le Gaelscoil Phádraig Naofa a cheannaigh ciliméadar de <USER> in Ard Mhacha
0	Podchraoltaí ar fáil anseo  <URL> <USER> <USER> <USER> <USER> <USER>
1	Duine de mhuintir an Oileáin -  Gearóid Cheaist Ó Catháin, in aonacht le Nuala de Búrca(IGL), Claire Ní Mhuirthile (IGL)is scoláirí idirnáisiúnta Ionad na Gaeilge Labhartha. ☘️🛶🗽🏑 <URL>
1	Beartaíocht múchta & moilleadóireachta ó <USER> ó thaobh thodchaí Oifig Poist, An Bhun Bhig  #MoillShíoraí
1	Faigh scéal iomlán bhliain peile na Dubs anseo - <URL> #UpTheDubs #GAA <URL>
~~~

**BibTeX**:
~~~
@misc{inscne,
 title = {Irish Twitter corpus labeled by surnames},
 author = {Scannell, Kevin},
 url = {https://github.com/kscanne/gbb/tree/main/datasets/inscne},
 copyright = {Copyright 2007-2022, All Rights Reserved},
 year = {2022} }
~~~
