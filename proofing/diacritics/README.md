## Diacritic Restoration

### Task Description
In the case of Irish, this problem takes a text in
which the fadas have been removed or omitted, and attempts to 
put them back. This is an important task because 
it's not at all unusual for Irish speakers to omit fadas when
typing the language, especially in informal contexts like social media.
Sometimes this is because their computer or mobile device is not
set up to produce fadas, or because they can only be produced through some 
clumsy method (like typing ALT+0225 for “á” on Windows). 

**Example input**:

~~~
Niorbh aon fhile e, ach rinne se eachtai.
~~~

**Desired output**:

~~~
Níorbh aon fhile é, ach rinne sé éachtaí.
~~~

I prefer the term “Unicodification” for this task,
because for many other languages it involves the restoration of
ASCII characters to proper Unicode forms that don't involve
diacritics at all, e.g. k → ƙ or d → ɗ in Hausa.
See [this paper](https://cs.slu.edu/~scannell/pub/lre.pdf)
for more details.

Irish texts sometimes contain Unicode characters from other
languages (“Gàidhlig”, “Měchura”, etc.) and these characters are 
“in play” for this task. The complete set of possible 
restorations is formally defined by the mappings in the script
`diacritization_stripping_data.py`.

There are many ambiguous cases in Irish, even among the top 1000 most
frequent words, that make this task challenging:
na/ná, mo/mó, i/í, do/dó, dar/dár, cead/céad, ar/ár, a/á, etc.
Out-of-vocabulary words present a challenge as well, but 
these can often be handled with a bit of modeling at the subword level.
For example, one would hope that a new term like “réamh-Bhreatimeacht”
could be handled properly based on having seen the prefix 
“réamh-” many times in training on other words.

### Evaluation Metrics

The primary metric we use to evaluate an algorithm on this task
is its word-level accuracy (**WLA** in the tables below);
we believe this gives more meaningful results than
metrics at the character level.
We also report precision and recall, again at the word level.
All results are reported as percentages.

### Algorithms

* **Accentuate**: This is the algorithm used by the Accentuate.us
web service. It is essentially a Bayesian classifer that incorporates
both character and word-level features. Full details available
in [this paper](https://cs.slu.edu/~scannell/pub/lre.pdf),
with source code available in
[this repository](https://sourceforge.net/projects/lingala/).
We report two sets of results for this algorithm. The row labeled simply
“Accentuate” refers to the algorithm when trained using
the training data for the benchmark dataset in question.
The row labeled “Accentuate (Pretrained)” refers to the algorithm 
when trained on a general Irish language corpus. The latter is
what is made available through the Accentuate.us public API.

* **Keep as ASCII**: This algorithm leaves the input text unchanged.
This gives an estimate of the percentage of words in Irish that
have no fadas.

* **Unigrams**: Given an ASCII-only input token *w*, this algorithm
chooses the most frequent word in the training set with asciification *w*.

### Results

There are currently **2** benchmarks for this task.

## tuairisc ([README](../../datasets/tuairisc/README.md))
|Algorithm|WLA|Precision|Recall|F<sub>1</sub>|
|---|---|---|---|---|
|Accentuate|98.66|96.36|97.99|97.17|
|Accentuate (Pretrained)|98.38|95.47|97.48|96.47|
|Unigrams|97.76|98.60|92.45|95.43|
|Keep as ASCII|74.29|nan|0.00|nan|

## charles ([README](../../datasets/charles/README.md))
|Algorithm|WLA|Precision|Recall|F<sub>1</sub>|
|---|---|---|---|---|
|Accentuate|97.83|94.30|96.30|95.29|
|Accentuate (Pretrained)|96.88|91.48|95.23|93.32|
|Unigrams|96.78|97.87|89.58|93.54|
|Keep as ASCII|72.70|nan|0.00|nan|
