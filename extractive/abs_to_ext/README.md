### Introduction

This code converts an abstractive gold standard summary to extractive. Given the full document and its abstractive gold standard summary, the code labels each sentence in the full document either 1 (meaning that it is a summary sentence) or 0 (meaning that it is not a summary sentence).

The extractive training data thus generated can be used to train extractive supervised summarization methods like [Gist](https://github.com/Law-AI/summarization/tree/aacl/extractive/Gist).

### Basic command to run:
`python extractive_labels.py /path/to/base/directory`

### To view other options (show help):
`python extractive_labels.py -h`

### External libraries required:
- numpy
- tqdm
- [rouge](https://pypi.org/project/rouge/)


### Method reference
You can use one of the two methods for generating labels:
- **avr_rg**: This method selects 3 sentences from the full text for each sentence in the summary wrt the highest average ROUGE scores. Ref: [Narayan.et.al. NAACL 2018](https://www.aclweb.org/anthology/N18-1158/)
- **m_rg**: This method selects greedily selects the maximal sentences from full text to maximize ROUGE scores wrt the summary. Ref: [Nallapati.et.al. AAAI 2017](https://ojs.aaai.org/index.php/AAAI/article/view/10958)
