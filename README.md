# iSRL data!

This is an attempt to provide a simple, replicable set of data for implicit semantic role labeling, with all of the dat annotated in -- or converted to -- the PropBank inventory. 

Some datasets exist for iSRL, but they (a) require that you dig into the FrameNet files or PTB files for their annotations, and (b) can be hard to evaluate.  This task is hard enough without that issue.  

I'm assuming the following aspects of this task:
* Assuming that each possible implicit role is given ("possible" == not explicitly mentioned). 
* That each role links to a list of spans in the prior text (usually constituting something like a coreference chain). 
* The task is for a model to predict a single span in that document which alignes with that role, if it recoverable at all. 
* 


