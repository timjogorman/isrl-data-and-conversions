# iSRL data!

This is an attempt to provide a simple, replicable set of data for implicit semantic role labeling, with all of the dat annotated in -- or converted to -- the PropBank inventory. 

The data is composed of:
- Conversions of two corpora (SemEval-2010-10 and Gerber and Chai 2012) into a simpler PropBank format, and into a simple format that marks spans in raw text files
- Conversion of the MS-AMR annotations into more traditional iSRL annotations.  
- A noisy, automatic conversion of some within-sentence AMR re-entrancies into iSRL annotations

I can't post the source text for the AMR or NomBank data, but there are scripts for pulling out the correct text and putting it into the right place, with the AMR 2017 release and the PTB3 (*not* ontonotes 5.0 -- the tokenizations are different between the two).  

I've also included a simple script '''evaluate-isrl.py''', which uses the simple dice score evaluation between a dataset and a set of predictions.  Since predicting into the XML is annoying, these will also accept a simple JSON format.  ``evaluation-examples'' contains a set of (poor) predictions which you should be able to run with:


python evaluate-isrl.py data/test/nombank/ evaluation-examples/test/nombank/

```precision 0.28194427158347196, recall 0.2655733138786252, and f1 0.27351404419393294```
python evaluate-isrl.py data/test/semeval/ evaluation-examples/test/semeval/

```precision 0.10199004975124379, recall 0.09234234234234236, and f1 0.09692671394799056```

python evaluate-isrl.py data/test/nombank/wsj_2398.xml evaluation-examples/test/nombank/wsj_2398.predicted.json

```precision 0.15018315018315015, recall 0.15018315018315015, and f1 0.15018315018315015```

There is also an ugly simple viewer for skimming these examples, which takes one of these xml files in data/ as an argument (once you've loaded the corresponding source files).
