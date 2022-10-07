# Introduction

This folder contains dataset of the paper *Legal Case Document Summarization: Extractive and Abstractive Methods and their Evaluation* accepted at AACL-IJCNLP 2022. The dataset repository can be downloaded from https://zenodo.org/record/7152317#.Yz6mJ9JByC0 .

There are 3 datasets :
- IN-Abs : Indian Supreme Court case documents & their *abstractive* summaries, obtained from http://www.liiofindia.org/in/cases/cen/INSC/
- IN-Ext : Indian Supreme Court case documents & their *extractive* summaries, written by two law experts (A1, A2).
- UK-Abs : United Kingdom (U.K.) Supreme Court case documents & their *abstractive* summaries, obtained from https://www.supremecourt.uk/decided-cases/

# Details of each dataset

## IN-Abs
We crawled 7,130 full case documents and their corresponding abstractive summaries from http://www.liiofindia.org/in/cases/cen/INSC/ .
Among them, 7030 (document, summary) pairs are randomly sampled as the training dataset. The remaining 100 (document, summary)
pairs are considered as the test set. The directory structure is as follows :


    .
    ├── train-data                    # folder contains documents and summaries for training
    │   ├── judgement              
    │   ├── summary             
    │   ├── stats-IN-train.txt        # text file containing the word and sentence count statistics of the documents
    └── test-data                     # folder contains documents and summaries for test
    │   ├── judgement              
    │   ├── summary
    │   ├── stats-IN-test.txt         # text file containing the word and sentence counts of the judgements & the summaries
    
## IN-Ext

This dataset contains 50 Indian Supreme Court case documents and their extractive summaries. For each document, there are two summaries written individually by two law experts A1 and A2. Each summary by each law expert is of two types : full & segment-wise.

- "full" : a coherent piece of summary.

- "segment-wise" : the following segments are considered -- 'analysis', 'argument', 'facts', 'judgement', 'statute'. A "full" summary is broken down into these segments. Each segment is a folder.

More details can be found in the associated README file of the dataset repository.

The directory structure is as follows :


    .
    ├── judgement                 # folder contains documents           
    ├── summary    
    │   ├── full                  # folder contains full summaries
    │   │   ├── A1
    │   │   ├── A2
    │   ├── segment-wise          # folder contains segment-wise summaries
    │   │   ├── A1
    │   │   ├── A2
    ├── IN-EXT-length.txt         # text file containing the word and sentence counts of the judgements & the summaries
    
## UK-Abs
We crawled 793 full case documents and their corresponding abstractive summaries from https://www.supremecourt.uk/decided-cases/ . Among them, 693 (document, summary) pairs are randomly sampled as the training dataset. The remaining 100 (document, summary) pairs are considered as the test set. 

Similar to IN-Ext, the summaries in the dataset are of two types -- full and segment-wise. 

The segments in the UK dataset are 'background' , 'judgement' and 'reasons'. The test-data folder contains these segment-wise and full summaries.

The directory structure is as follows :


    .
    ├── train-data                    # folder contains documents and summaries for training
    │   ├── judgement              
    │   ├── summary             
    │   ├── stats-UK-train.txt        # text file containing the word and sentence count statistics of the documents
    └── test-data                     # folder contains documents and summaries for test
    │   ├── judgement              
    │   ├── summary
    │   │   ├── full                  # folder contains full summaries
    │   │   ├── segment-wise          # folder contains segment-wise summaries
    │   ├── stats-UK-test.txt         # text file containing the word and sentence counts of the judgements & the summaries
    
# Citation
If you are using the dataset, please refer to the following paper:
```
@inproceedings{bhattacharya2021,
  title={Legal Case Document Summarization: Extractive and Abstractive Methods and their Evaluation},
  author={Shukla, Abhay and Bhattacharya, Paheli and Poddar, Soham and Mukherjee, Rajdeep and Ghosh, Kripabandhu and Goyal, Pawan and Ghosh, Saptarshi},
  booktitle={The 2nd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 12th International Joint Conference on Natural Language Processing},
  year={2022}
}

