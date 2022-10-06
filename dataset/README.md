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

[`get-n-grams.py`](get-n-grams.py) extracts the top ngrams across each category. It avoids a n-gram to be constructed purely of stop words, like *the*, *an*.

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
# Top bigrams
$ python get-n-grams.py 2
```

Ohtermax indicates the maximum frequency for that n-gram in other categories, which helps us decide whether that n-gram can be used as a cue phrase or not. Some sample Top n-grams can be found in [top_ngrams/](top_ngrams/) folder. The finalized cues are subsequently identified (manually, after the automated n-gram detection is executed) and stored in [`formulated_constants.py`](formulated_constants.py).

The following algorithms require a FullText_html folder and a caseanalysis folder, which we have scraped from WestLaw India. Due to its huge size, we have not made those files available on GitHub. Our training dataset consists of 23 documents, in the `annotated` and `annotated_json` files, and test size is 7820 documents, legal documents dating from the years 2010-2018.

#### Execution

If you wish to extract Ngrams from scratch, please follow the following guidelines. This step is not required if you wish to only generate the summary with pre-trained models.
```py
$ python get-n-grams.py 1
$ python get-n-grams.py 2
$ python get-n-grams.py 3
$ python get-n-grams.py 4
```

We need to manually enter the desired cues in formulated_constants.py.