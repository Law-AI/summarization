### Usage :

*import using the following line:*
`from split_sentences import custom_tokenizer
tokenizer = custom_tokenizer()`

## Split a document into sentences only
`with open("document.txt") as fp:
    sents = tokenizer.to_sentences(fp.read().replace('\n', ' '))`

## Split a document into sentences and normalize the text
`with open("document.txt") as fp:
    cleaned_sents = tokenizer.to_cleaned_sents(fp.read().replace('\n', ' '))`

