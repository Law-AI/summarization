# CaseSummarizer

This repository contains an implementation of the paper [CaseSummarizer](http://www.aclweb.org/anthology/C16-2054)

A sample input file, along with its pre-processing output and summary is present in the sample folders.

### (Optional) Preprocess the documents 
Description : Tokenize, lemmatize, remove stopwords

#### Run : 
```
python preprocess.py    path/to/input/folder/   path/to/output/folder
```

### Generate Summary :

#### Run : 
```
python summary.py    path/to/input/folder/    path/to/output/folder/   path/to/dictionary.txt/file/
python summary_length.py  path/to/original/doc/folder/    path/to/output/folder/from/summary.py/   path/to/output/folder/    fraction/of/original/text/length/as/summary
```

### Prerequisites
 * [Python 2.7+](https://www.python.org/download/releases/2.7/)
 * [Numpy](http://www.numpy.org/)
 * [NLTK](http://www.nltk.org/)
