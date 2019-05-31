# iSRL data!

This is an attempt to provide a simple version of the datasets involved with implicit SRL, and access to a surface-form conversion of the implicit role annotations from MS-AMR. These are all put into a somewhat simplistic format so that the input is the same for all sets -- a list of unstated implicit roles under consideration, PropBank arguments defining each role, and spans in the text that those roles refer to. 

The data is composed of:
- Conversions of two corpora (SemEval-2010-10 and Gerber and Chai 2012) into a simpler PropBank format, and into a simple format that marks spans in raw text files
- Conversion of the MS-AMR annotations onto surface forms (slightly noisy due to automatic alignment)
- A noisy, automatic conversion of some within-sentence AMR re-entrancies into iSRL annotations


I can't post the source text for the AMR or Beyond NomBank data, but there are scripts for pulling the text out of their respective corpora and putting them into the right place -- using the AMR 2017 release and the PTB3, respectively (*not* OntoNotes 5.0 -- tokenization changed between PTB3 and ON5, so that would mess with the token offsets).  

I've also included a script, ```evaluate-isrl.py```, which implements the simple dice score evaluation.  It can deal with a number of formats -- either the big XMLs I used for the data, or simple json or txt files.  ``evaluation-examples'' contains a set of (poor) predictions which you should be able to run with this script, which also provide examples of the format:

python evaluate-isrl.py data/test/nombank/ evaluation-examples/test/nombank/

```precision 0.28194427158347196, recall 0.2655733138786252, and f1 0.27351404419393294```
python evaluate-isrl.py data/test/semeval/ evaluation-examples/test/semeval/

```precision 0.10199004975124379, recall 0.09234234234234236, and f1 0.09692671394799056```

python evaluate-isrl.py data/test/nombank/wsj_2398.xml evaluation-examples/test/nombank/wsj_2398.predicted.json

```precision 0.15018315018315015, recall 0.15018315018315015, and f1 0.15018315018315015```

python evaluate-isrl.py data/test/nombank/wsj_2398.xml evaluation-examples/wsj_2398.txt

```precision 0.15018315018315015, recall 0.15018315018315015, and f1 0.15018315018315015```


There is also an ugly simple viewer for skimming these examples, which takes one of these xml files in data/ as an argument (once you've loaded the corresponding source files).
