### Gist

Implementation of the paper [Extracting the Gist of Chinese Judgments of the Supreme Court](https://dl.acm.org/doi/10.1145/3322640.3326715), ICAIL 2019

Like all extractive supervised summarization methods, the training data for the model should be sentences labelled 0 (not a summary sentence) or 1 (summary sentence). 

We may use the [extractive_labels.py](https://github.com/Law-AI/summarization/blob/aacl/extractive/abs_to_ext/extractive_labels.py) code to create this training data.

### Generate the handcrafted features for the training set

`python generate_features.py --data_path /path/to/train/documents/ --features_path /outpath/of/train/features/ --important_words cue_phrases.txt --pos_tags postags.txt --w2v True`
[if a pretrained word2vec model is not present, a model is trained based on the training set corpus]

`python generate_features.py --data_path /path/to/train/documents/ --features_path /outpath/of/train/features/ --important_words cue_phrases.txt --pos_tags postags.txt --word2vec_path /path/to/trained/word2vec/model.bin`
[if a pretrained word2vec model is present, mention its path]

### Train the LGBM classifier
`python train.py --data_path /path/to/train/documents/ --features_path /outpath/of/train/features/ --model_path /path/to/save/learned/model/`

*To view other options (show help):*
`python train.py -h`


### Generate the handcrafted features for test set

`python generate_features.py --data_path /path/to/test/documents/ --features_path /outpath/of/test/features/ --important_words cue_phrases.txt --pos_tags postags.txt --word2vec_path /path/to/trained/word2vec/model.bin`

### Infer summaries using the trained LGBM classifier

`python infer.py --data_path /path/to/test/documents/ --features_path /outpath/of/test/features/ --summary_path /path/to/save/summaries/ --model_path /path/to/trained/model.pkl --length_file /path/to/summary/length/file`
The prediction probability of each sentence in stored in /outpath/of/test/features/pred_scores/ [this directory is automatically created]

- The trained model has been made publicly available at https://zenodo.org/record/7234359#.Y2fx09JBy-o


### format of length file

```
filename <TAB> required-summary-length-in-words
```
### External libraries required

- lightgbm = 2.3.1
- sklearn = 0.21.3
- gensim = 3.4.0
- tqdm
