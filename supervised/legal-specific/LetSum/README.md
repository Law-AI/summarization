# Algorithm: LetSum

[LetSum, a Text Summarization system in Law field - Farzindar, A., and G. Lapalme](http://rali.iro.umontreal.ca/rali/?q=en/node/673)

## Execution

``` 
$ python
>>> import letsum
>>> import letsum_test
>>> summary = letsum_test.LetSum('sample input.txt')
```

We use ROUGE as a metric of summary evaluation. The top level file here is [letsum.py](letsum.py), which loops over all the testing documents, generates a summary, compares it with the manually annotated summary provided by WestLaw, computed and reports the ROUGE score for each document. Following is an explanation of how the top level file operates.

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

