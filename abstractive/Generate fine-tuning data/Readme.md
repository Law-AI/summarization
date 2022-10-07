#Scripts and codes

gen_fine_tuning_data_CLS.ipynb - Script to generate fine tuning data using CLS similarity method

gen_fine_tuning_data_MCS.ipynb - Script to generate fine tuning data using MCS similarity method

gen_fine_tuning_data_SIF.ipynb - Script to generate fine-tuning data using SIF similarity method

gen_fine_tuning_data_MCS_RR.ipynb - Script to generate fine-tuning data using MCS similarity method and rhetorical role-based segmenting


#Requirements

transformers  4.12.3
pytorch  1.10
pytorch lightning  1.5.1
bert-extractive-summarizer 0.9.0

#Usage

1. Change the path variable to the path of the dataset in utilities.py
2. Add the UK_freq.json or IN_freq.json to the folder
2. Follow the instructions given in the notebooks

Note that rhetorical role-based segmenting requires rhetorical role labeled documents. Each line in the document would contain a sentence, \t, and the label (sentence_1\tlabel).  

Rhetorical role labeling - https://link.springer.com/article/10.1007/s10506-021-09304-5 