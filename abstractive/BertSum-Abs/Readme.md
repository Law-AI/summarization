#Scripts and codes

PreSumm - Contains the dev branch of https://github.com/nlpyang/PreSumm

Chunker.ipynb - Script to form chunks from text files

#Requirements

multiprocess 0.70.9
numpy 1.17.2
pyrouge 0.1.3
pytorch-transformers 1.2.0
tensorboardX 1.9
torch 1.1.0

#Usage

1. Change the path variable to the path of the dataset in utilities.py
2. Use Chunker to chunk the input documents into chunk files
3. Use PreSumm to generate summaries for the chunk files