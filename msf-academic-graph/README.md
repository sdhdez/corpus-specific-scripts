#corpus-specific-scripts/msf-academic-graph

Scripts to pre-process the [Microsoft Academic Graph](https://academicgraph.blob.core.windows.net/graph-2016-02-05/index.html). 

## mag-titles-pos.py

### Description

Script to get the part-of-speech of English titles in the Microsoft Academic Graph corpus. 

It uses guess_language for English identification, TreebankWordTokenizer as tokenizer and nltk.tag.perceptron as POS tagger.

### Usage

```
$ python mag-titles-pos.py [-s <integer>] [-t <integer>] <path/to/input> [path/to/output]
```
For example:

```
$ python mag-titles-pos.py Papers.txt
Status: 14/08/2016 22:11:03 Count: 0
01B27BE8
Evaluating VBG
Polarity NNP
for IN
Verbal NNP
Phraseological NNP
Units NNS

027D0030
Automatic JJ
Monitoring VBG
the DT
Content NNP
of IN
Audio NNP
Broadcasted NNP
by IN
Internet NNP
Radio NNP
Stations NNP

7CFE299E
Towards NNS
a DT
set NN
of IN
Measures NNS
for IN
Evaluating NNP
Software NNP
Agent NNP
Autonomy NNP

59BEBE1C
Learning VBG
Probability NNP
Densities NNP
of IN
Optimization NNP
Problems NNP
with IN
Constraints NNP
and CC
Uncertainty NNP

5873C011
Towards IN
a DT
Model NNP
for IN
an DT
Immune NNP
System NN

...

```

The logging information is sent to *stderr*, the rest to *stdout* or the given file.

You might want to get the POS of an especific number titles or to skip some of them. You can do this with the options  and **-t** (take) and **-s** (skip).

```
$ python mag-titles-pos.py -s 2 -t 3 Papers.txt
Status: 14/08/2016 22:19:30 Count: 0
7CFE299E
Towards NNS
a DT
set NN
of IN
Measures NNS
for IN
Evaluating NNP
Software NNP
Agent NNP
Autonomy NNP

59BEBE1C
Learning VBG
Probability NNP
Densities NNP
of IN
Optimization NNP
Problems NNP
with IN
Constraints NNP
and CC
Uncertainty NNP

5873C011
Towards IN
a DT
Model NNP
for IN
an DT
Immune NNP
System NN

Status: 14/08/2016 22:19:30 Final: 5 0

```

The corpus is big, so you might want to keep it compressed, this is possible with *bash*.

```
$ python mag-titles-pos.py <(zcat ~/MicrosoftAcademicGraph/Papers.txt.gz) | gzip -c > pos.txt.gz 
```
