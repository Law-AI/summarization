# Introduction

This repository contains implementations and datasets made available in the following papers :

- Legal Case Document Summarization: Extractive and Abstractive Methods and their Evaluation accepted at AACL-IJCNLP 2022.
- A Comparative Study of Summarization Algorithms Applied to Legal Case Judgments accepted at ECIR 2019.

We provide the code base of various Extractive and Abstractive summarization algorithms applied to legal case documents. We also provide three summarization datasets from the Indian and UK Supreme Court case documents.

# Dataset

We make available 3 legal document summarization datasets. Please refer to the *dataset* folder for more details :

- IN-Abs : Indian Supreme Court case documents & their *abstractive* summaries, obtained from http://www.liiofindia.org/in/cases/cen/INSC/
- IN-Ext : Indian Supreme Court case documents & their *extractive* summaries, written by two law experts (A1, A2).
- UK-Abs : United Kingdom (U.K.) Supreme Court case documents & their *abstractive* summaries, obtained from https://www.supremecourt.uk/decided-cases/


# Extractive Summarization methods

We provide the implementations of the following methods in the *extractive* folder of the repository :

- [Improving Legal Document Summarization Using Graphical Models](https://www.cse.iitm.ac.in/~ravi/papers/Saravanan_jurix_06.pdf), JURIX 2006
- [LetSum, a Text Summarization system in Law field](http://rali.iro.umontreal.ca/rali/?q=en/node/673), JURIX 2004
- [CaseSummarizer](http://www.aclweb.org/anthology/C16-2054), COLING 2016
- [Automatic Summarization of Legal Decisions using Iterative Masking of Predictive Sentences](https://dl.acm.org/doi/10.1145/3322640.3326728), ICAIL 2019
- [Extracting the Gist of Chinese Judgments of the Supreme Court](https://dl.acm.org/doi/10.1145/3322640.3326715), ICAIL 2019 
- [Extractive Summarization using Deep Learning](https://arxiv.org/pdf/1708.04439.pdf), arXiv preprint, 2017
- We also provide the script to convert an abstractive gold standard summary to extractive, for training supervised extractive summarization methods.


# Abstractive Summarization methods

- Scripts to generate fine tuning data using following techniques
  - CLS
  - SIF
  - MCS
  - MCS_RR
- Scripts to fine-tune following models
  - [BART](https://huggingface.co/facebook/BART_large)
  - [legal-Pegasus](https://huggingface.co/nsi319/legal-pegasus)
  - [Legal-LED](https://huggingface.co/nsi319/legal-led-base-16384)
- Scripts to generate summaries using following models/methods 
  - BART(CLS, MCS, SIF)
  - BART_RR
  - BERT-BART
  - Legal-LED
  - Pegasus
- Helper chunking and combiner scripts for BertSum-Abs and Pointer Generator methods

# Availability of Trained Models

The following models trained on the IN-Abs & UK-Abs datasets are publicly available at https://zenodo.org/record/7234359#.Y2tShdJByC1

- Extractive : SummaRuNNer, Gist

- Abstractive : Legal-Pegasus, Legal-LED

<!-- ## References

- [Enhancing Unsupervised Sentence Similarity Methods with Deep Contextualised Word Representations](https://acl-bg.org/proceedings/2019/RANLP%202019/pdf/RANLP115.pdf), RANLP 2019
- [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084), EMNLP 2019 --> 

# Citation
If you are using the implementations / datasets / trained models, please refer to the following papers:
```
@inproceedings{shukla2022,
  title={Legal Case Document Summarization: Extractive and Abstractive Methods and their Evaluation},
  author={Shukla, Abhay and Bhattacharya, Paheli and Poddar, Soham and Mukherjee, Rajdeep and Ghosh, Kripabandhu and Goyal, Pawan and Ghosh, Saptarshi},
  booktitle={The 2nd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 12th International Joint Conference on Natural Language Processing},
  year={2022}
}

@inproceedings{bhattacharya2019comparative,
  title={A comparative study of summarization algorithms applied to legal case judgments},
  author={Bhattacharya, Paheli and Hiware, Kaustubh and Rajgaria, Subham and Pochhi, Nilay and Ghosh, Kripabandhu and Ghosh, Saptarshi},
  booktitle={European Conference on Information Retrieval},
  pages={413--428},
  year={2019},
  organization={Springer}
}
```

