# TextSummarizer
Source code of the paper [Extractive Summarization using Deep Learning](https://arxiv.org/pdf/1708.04439.pdf)

Description: Used two layers of Restricted Boltzmann Machine as a Deep Belief Network to enhance and abstract various features such as named entities, proper nouns, numeric tokens, sentence position etc. to score sentences then selecting the top scores, hence producing an extractive summary.

## Prerequisites
 * [Python 2.7+](https://www.python.org/download/releases/2.7/)
 * [Numpy](http://www.numpy.org/)
 * [Scipy](https://www.scipy.org/)
 * [Theano](https://github.com/Theano/Theano)
 * [NLTK](http://www.nltk.org/)

## Getting Started
 1. Clone this repository <br>
    `git clone https://github.com/vagisha-nidhi/TextSummarizer.git`<br>
 2. Place your sample text files in `./articles` folder. Some sample articles are already kept for convenience.<br>
 3. Run `python Summarizer.py` to summarize the articles.<br>
 4. You will get the summarized outputs in `./outputs` folder.
 
## Example 
 Sample input and output examples have been given in [this](https://github.com/vagisha-nidhi/TextSummarizer/blob/master/input-output.pdf) along with enhanced feature matrix for the articles.
