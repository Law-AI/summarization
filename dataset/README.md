This folder contains dataset of the paper *Legal Case Document Summarization: Extractive and Abstractive Methods and their Evaluation* accepted at AACL-IJCNLP 2022.

There are 3 datasets :
- IN-Abs : Indian Supreme Court case documents & their `abstractive' summaries, obtained from http://www.liiofindia.org/in/cases/cen/INSC/
- IN-Ext : Indian Supreme Court case documents & their `extractive' summaries, written by two law experts (A1, A2).
- UK-Abs : United Kingdom (U.K.) Supreme Court case documents & their `abstractive' summaries, obtained from https://www.supremecourt.uk/decided-cases/

# Details of each dataset

## IN-Abs
We crawled 7,130 full case documents and their corresponding abstractive summaries from http://www.liiofindia.org/in/cases/cen/INSC/ . Among them, 7030 (document, summary) pairs are randomly sampled as the training dataset. The remaining 100 (document, summary) pairs are considered as the test set. The directory structure is as follows :

IN-Abs                
├── train-data              # folder contains documents and summaries for training
│   ├── judgement           # folder contains documents (sentence splitted)
│   ├── summary             # folder contains summaries (sentence splitted)
│   ├── stats-IN-train.txt  # text file containing the word and sentence count statistics of the documents
│
├── test-data               # folder contains documents and summaries for test/evaluation (100 docs)
    ├── judgement           # folder contains documents (sentence splitted)
    ├── summary             # folder contains summaries (sentence splitted)
    ├── stats-IN-test.txt   # text file containing the word and sentence count statistics of the documents
   
   
## IN-Ext
This dataset contains 50 Indian Supreme Court case documents and their extractive summaries. For each document, there are two summaries written individually by two law experts A1 and A2. Each summary by each law expert is of two types : full & segment-wise.
"full" : a coherent piece of summary.
"segment-wise" : the following segments are considered -- 'analysis', 'argument', 'facts', 'judgement', 'statute'. A "full" summary is broken down into these segments. Each segment is a folder.
For a particular document, appending the "segment-wise" summaries results in a "full" summary. 
As an example, consider the document 1953_L_1.txt. We have the full text of the document in the "judgement" folder. The "summary" folder contains two sub-folders "full" and "segment-wise". Under each subfolder, there are two subfolders "A1" and "A2" .
summary/full/A1/1953_L_1.txt --> contains the full summary of 1953_L_1.txt written by A1.
summary/full/A2/1953_L_1.txt --> contains the full summary of 1953_L_1.txt written by A2.

summary/segment-wise/A1/analysis/1953_L_1.txt --> "analysis" segment of the summary written by A1
summary/segment-wise/A1/argument/1953_L_1.txt -->  "argument" segment of the summary written by A1
summary/segment-wise/A1/facts/1953_L_1.txt -->  "facts" segment of the summary written by A1
summary/segment-wise/A1/judgement/1953_L_1.txt -->  "judgement" segment of the summary written by A1
summary/segment-wise/A1/statute/1953_L_1.txt -->  "statute" segment of the summary written by A1

summary/segment-wise/A2/analysis/1953_L_1.txt --> "analysis" segment of the summary written by A2
summary/segment-wise/A2/argument/1953_L_1.txt -->  "argument" segment of the summary written by A2
summary/segment-wise/A2/facts/1953_L_1.txt -->  "facts" segment of the summary written by A2
summary/segment-wise/A2/judgement/1953_L_1.txt -->  "judgement" segment of the summary written by A2
summary/segment-wise/A2/statute/1953_L_1.txt -->  "statute" segment of the summary written by A2

The directory structure is as follows :

IN-Ext                
├── judgement             # folder contains documents 
│   
├── summary              # folder contains summaries 
│    ├── full             # folder contains full summaries 
│    │	  ├── A1
│    │	  ├── A2
│    ├── segment-wise
│    │	  ├── A1
│    │	  ├── A2            
├── IN-EXT-length.txt   # text file containing the word and sentence count statistics of the documents

## UK-Abs
We crawled 793 full case documents and their corresponding abstractive summaries from https://www.supremecourt.uk/decided-cases/ . Among them, 693 (document, summary) pairs are randomly sampled as the training dataset. The remaining 100 (document, summary) pairs are considered as the test set. Similar to IN-Ext, the summaries in the dataset are segment-wise. The segments in the UK dataset are 'background' , 'judgement' and 'reasons'. The test-data folder contains these segment-wise and full summaries.

The directory structure is as follows :

UK-Abs                
├── train-data              # folder contains documents and summaries for training
│   ├── judgement           # folder contains documents 
│   ├── summary             # folder contains summaries 
│   ├── stats-UK-train.txt  # text file containing the word and sentence count statistics of the documents
│
├── test-data               # folder contains documents and summaries for test/evaluation (100 docs)
    ├── judgement           # folder contains documents 
    ├── summary             
    │	   ├── full	    # folder contains full summaries 
    │	   ├── segment-wise # folder contains segment-wise summaries
    ├── stats-UK-test.txt   # text file containing the word and sentence count statistics of the documents
   

