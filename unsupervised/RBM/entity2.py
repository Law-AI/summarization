import nltk 

sample = "Narenda Modi is the pm of India"

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names
def ner(sample):
    try:
        sentences = nltk.sent_tokenize(sample)
    except:
        raise Exception
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)



    entity_names = []
    for tree in chunked_sentences:
    # Print results per sentence
    # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))
    print set(entity_names)
    return len(entity_names)