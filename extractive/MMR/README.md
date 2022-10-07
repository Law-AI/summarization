### Basic command to run:
`python MMR.py --data_path /path/to/documents/ --summary_path /path.to/save/summaries/ --length_file lengthfile.txt`


*format of length file*
<filename> tab <required-summary-length-in-words>

### External libraries required

- spacy = 2.2.3
- nltk = 3.5
- sklearn = 0.21.3
- tqdm