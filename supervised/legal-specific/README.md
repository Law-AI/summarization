# Supervised summarization algorithms

We implement the Graphical Model implemented by [Saravanan et. al](https://www.cse.iitm.ac.in/~ravi/papers/Saravanan_jurix_06.pdf), and [LetSum](http://rali.iro.umontreal.ca/rali/?q=en/node/673), which both depend on pre-identified cue words. Since the domain of cases the previous works varied hugely with the focus of domains, we started out with identification of cue words.

## Identification of cue words (common to both algorithms)

We start off with labelled data in the format
`S1 I The question in this appeal is whether the grant of a mining lease for a period of ten years by the assessee can give rise to a capital gain taxable under section 45 of Income-tax Act, 1961.`

or 
```
{
            "label": [
                "Ruling by the present court"
            ],
            "points": [
                {
                    "start": 11683,
                    "end": 12929,
                    "text": " As can be seen from the reading of the aforesaid portion of the circular, the issue was examined after keeping in mind judgments of CESTAT in Gujarat Ambuja Cement Ltd. and M/s. Ultratech Cement Ltd. Those judgments, obviously, dealt with unamended Rule 2(l) of Rules, 2004. The three conditions which were mentioned explaining the 'place of removal' are defined in Section 4 of the Act. It is not the case of the Department that the three conditions laid down in the said Circular are not satisfied. If we accept the contention of the Department, it would nullify the effect of the word 'from' the place of removal appearing in the aforesaid definition. Once it is accepted that place of removal is the factory premises of the assessee, outward transportation 'from the said place' would clearly amount to input service. That place can be warehouse of the manufacturer or it can be customer's place if from the place of removal the goods are directly dispatched to the place of the customer. One such outbound transportation from the place of removal gets covered by the definition of input service.\n9. We, thus, do not find any infirmity in the impugned judgment. Appeals are devoid of any merit and are accordingly dismissed.\nAppeals dismissed"
                }
            ]
        }
```

The annotated data lies in [annotated/](annotated/) and [annotated_json/](annotated_json/) folders, corresponding to dataset provided by FIRE legal track, and annotations we obtained via legal experts respectively.

Extraction of most common n-grams (unigram, bigram, trigram, 4-grams) from the text is performed, for each category.

### Categories

Since supervised algorithms in summarization are template-filling tasks, we follow the categorization provided by [Fire Legal Track 2013](https://www.isical.ac.in/~fire/2013/legal.html), which is as follows:

| Category | Code |
| --- | --- |
| Facts | F (FI / FE) |
| Issue | I | 
| Argument | A |
| Ruling by lower court | LR |
| Statute | SS |
| Precedent | SP |
| Other general standards, including customary, equitable and other extra-legal considerations | SO |
| Ruling by the present court | R |


### Category extraction 

We first need to separate out texts in documents according to their categories. This is done by [`extract-categories.py`](extract-categories.py), which stores the category wise text in a [categories/](categories/) folder, used ahead.

### Extraction of n-grams

[`get-n-grams.py`](get-n-grams.py) extracts the top unigrams across each category. It avoids a n-gram to be constructed purely of stop words, like *the*, *an*.

```
# Get top unigrams for all categories
$ python get-n-grams.py 1
# Truncated output, only unary displayed here
 I
+--------+----+-------------+----+----+----+
| Phrase | I  | Othermax  R | SO | SP | SS |
+--------+----+-------------+----+----+----+
| forest | 11 |    6      4 | 0  | 6  | 1  |
| lands  | 13 |    6      1 | 0  | 4  | 2  |
|  and,  | 7  |    6      3 | 2  | 4  | 1  |
+--------+----+-------------+----+----+----+
```

Ohtermax indicates the maximum frequency for that n-gram in other categories, which helps us decide whether that n-gram can be used as a cue phrase or not. Some sample Top n-grams can be found in [top_ngrams/](top_ngrams/) folder. The finalized cues are subsequently identified (manually, after the automated n-gram detection is executed) and stored in [`formulated_constants.py`](formulated_constants.py).

The following algorithms require a FullText_html folder and a caseanalysis folder, which we have scraped from WestLaw India. Due to its huge size, we have not made those files available on GitHub. Our training dataset consists of 23 documents, in the `annotated` and `annotated_json` files, and test size is 7820 documents, legal documents dating from the years 2010-2018.

## Algorithm: Graphical Model

[Paper](https://www.cse.iitm.ac.in/~ravi/papers/Saravanan_jurix_06.pdf)

The following code assumes the reader has some basic understanding of the algorithm beforehand.

We use ROUGE as a metric of summary evaluation. The top level file here is [rouge_crf.py](rouge_crf.py), which loops over all the testing documents, generates a summary via Graphical Model (CRF - Conditional Random Field), compares it with the manually annotated summary provided by WestLaw, computed and reports the ROUGE score for each document. 

The sample output is available at [`results_crf.txt`](results_crf.txt). The process fo generating summary for a legal document involves the following steps:

* Training the CRF (one time, for all test documents)
* Getting predicted categories for each sentence
* Rank sentences on importance based on K-mixture model
* Return summary based on max length of summary allowed

### Training the CRF

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

### Predicting categories / classes

Once the CRF model is trained, for a test document we obtain the features as well as the classification via [`crf_test.py`](crf_test.py).
In the current state, the test documents are HTML files, as in [`input_sample_test.html`](input_sample_test.html). The sccript handles HTML parsing and tokenization as well. The output of this script is the tokenized text, features, and category predictions for each statement.

### Rank sentences

After obtaining the predicted classes for a test document, we need to rank the sentences on basis of importance. We use K-mixture model to do this, the code for which is available as [`k_mix_model_test.py`](k_mix_model_test.py). The returned value is a mapping of each sentence and its score based on the heuristic function, which utilizes TF-IDF: 
```
K mixture model: Probability of word wi appearing k times is given as :
Pi(k) = (1-r) δk, 0 + (r / s+1) * (s / s+1)^k

δk, 0 = 1 iff k = 0, else 0
r = observed mean                s = observed IDF
```

### Generating the summary

We rank the sentences based on their KMM score (obtained above), and keep adding sentences in a decreasing order of their scores, as long as the template length of summary is not filled. Have a look at [`rouge_crf.py`](rouge_crf.py)'s `get_summary` function to have a look how this is implemented.


## Algorithm: LetSum

[Paper](http://rali.iro.umontreal.ca/rali/?q=en/node/673)

We use ROUGE as a metric of summary evaluation. The top level file here is [rouge_letsum.py](rouge_letsum.py), which loops over all the testing documents, generates a summary, compares it with the manually annotated summary provided by WestLaw, computed and reports the ROUGE score for each document. 

The sample output is available at [`results_letsum.txt`](results_letsum.txt). The summary is generated as follows:

We first define the mapping as done previously in the following order:

| FIRE category | Equivalent LetSum category |
| --- | --- |
| Facts | Introduction |
| Issue | Introduction |
| Arguments | Context |
| Ruling by lower court | Context |
| Statute | Analysis |
| Precedent | Analysis |
| Other general standards | Conclusion |
| Ruling by present court | Conclusion |

This is required since LetSum follows a template filling task, where each theme is allotted a percentage of the total length of permissible summary:

| Category | Percentage in summary |
| --- | --- |
| Introduction | 10 |
| Context | 24 |
| Analysis | 60 |
| Conclusion | 6 |
| Citation | 0 |

The total length of summary is restricted to *34%* of the total document length. Note that unlike Graphical Model, we do not need to train any model beforehand.

[`letsum_test.py`](letsum_test.py) expects an argument, in form of [`input_sample_test.html`](input_sample_test.html), for the legal document to be summarized. 

### Labelling each sentence

For each sentence in the document, we compute a score for that sentence indicating the number of cue phrases / cue pairs present in that sentence. The category with highest score is assigned as the label for that sentence (Introduction/Context/..). In the absence of any cues, a default label of _Context_ is assigned to the sentence.

### Ranking importance of sentences

Once the categories for each sentence has been identified, we want to retrieve the most relevant phrases within that category. Importance is assigned via a heuristic function, consisting of position of paragraph in document, position of sentence in paragraph, TF-IDF, and other factors. However, this function was not available, due to which we rank sentences based on their TF-IDF scores within each category. Hear, we avoid ranking stop words to keep the summary as informative as possible.

### Generating the summary

After ranking the phrases/ words in order of their TF-IDF scores within each category, we sort them in decreasing order and keep adding phrases in the output summary until the threshold of words in that category is reached. 

Say, for instance, a document of length 1600 words will have a summary of at most 1600*34% = 544 words, of which Context will be 24% = 130 words. In the decreasing order of TF-IDF scores, we keep adding words belonging to the category of "Context" until the output summary has less than 130 words.

### Grammatic modifications

Since the phrases might not make sense on their own, certain grammatic corrections have to be made in order for the summary to make sense. However, no further work from the Authors of LetSum focused on this aspect, due to which this phase was not applied in our work.

