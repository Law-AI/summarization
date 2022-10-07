# GraphicalModel

Implementation of the paper [Improving Legal Document Summarization Using Graphical Models](https://www.cse.iitm.ac.in/~ravi/papers/Saravanan_jurix_06.pdf), JURIX 2006

## Execution

```py
$ python
>>> import graphicalModel
>>> summary = graphicalModel.get_summary('sample input.txt')
```

The following code assumes the reader has some basic understanding of the algorithm beforehand. The above instruction is the only step needed to extract tehe summary, the following is just an explanation of [graphicalModel.py](graphicalModel.py)

We use ROUGE as a metric of summary evaluation. The top level file here is [graphicalModel.py](graphicalModel.py), which loops over all the testing documents, generates a summary via Graphical Model (CRF - Conditional Random Field), compares it with the manually annotated summary provided by WestLaw, computed and reports the ROUGE score for each document. 

The sample output is available at [`results_crf.txt`](results_crf.txt). The process fo generating summary for a legal document involves the following steps:

* Training the CRF (needs to be trained just once, for all test documents)
* Getting predicted categories for each sentence
* Rank sentences on importance based on K-mixture model
* Return summary based on max length of summary allowed

## Training the CRF

Saravnan et. al defined their own thematic roles / sections different than the one we followed, thus the first step was creating an equivalent mapping, which was as follows:

| Graphical Model category | Equivalent FIRE category |
| --- | --- |
| Identifying facts | Facts |
| Establishing facts | Issue |
| Arguing | Precedent |
| Arguments | Arguments |
| History | Ruling by lower court |
| Arguments | Other general standards |
| Ratio | Statute |
| Final Decision | Ruling by present court |

The features we use for training our CRF are:
* The word, in lower case
* Last 3 characters of words (to detect suffixes like -ion, -ing)
* Last 2 characters (suffixes, like -ed)
* Whether word w is all capital (abbreviation)
* Whether w is a string or number
* Position of w within sentence
* Position of paragraph in the document
* POS tag
* Presence of aforementioned cues
* Beginning / End of sentence ?
* The words surrounding w, i.e, the previous and the next word

This is done via [crf_train.py](crf_train.py), which runs the training algorithm for all annotated documents in `annotated` and `annotated_json` folder. The learned model is then saved in [`crf_alltrain.model`](crf_alltrain.model)

## Predicting categories / classes

Once the CRF model is trained, for a test document we obtain the features as well as the classification via [`crf_test.py`](crf_test.py).
In the current state, the test documents are HTML files, as in [`input_sample_test.html`](input_sample_test.html). The sccript handles HTML parsing and tokenization as well. The output of this script is the tokenized text, features, and category predictions for each statement.

## Rank sentences

After obtaining the predicted classes for a test document, we need to rank the sentences on basis of importance. We use K-mixture model to do this, the code for which is available as [`k_mix_model_test.py`](k_mix_model_test.py). The returned value is a mapping of each sentence and its score based on the heuristic function, which utilizes TF-IDF: 
```
K mixture model: Probability of word wi appearing k times is given as :
Pi(k) = (1-r) δk, 0 + (r / s+1) * (s / s+1)^k

δk, 0 = 1 iff k = 0, else 0
r = observed mean                s = observed IDF
```

## Generating the summary

We rank the sentences based on their KMM score (obtained above), and keep adding sentences in a decreasing order of their scores, as long as the template length of summary is not filled. Have a look at [`graphicalModel.py`](graphicalModel.py)'s `get_summary` function to have a look how this is implemented.
