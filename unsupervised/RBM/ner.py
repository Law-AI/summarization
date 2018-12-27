import nltk


# tokenize doc
with open('Texts/Text_1.txt','r') as f:
	doc = f.read()

sent_text = nltk.sent_tokenize(doc)

op = ""

for sent in sent_text:
  tokenized_text = nltk.word_tokenize(sent)
  num_present = [(x in summ_word_tokens) for x in tokenized_text]
  num_present = sum(num_present * 1)
  if num_present / len(tokenized_text) < 0.25:
    score = 0
  elif num_present / len(tokenized_text) > 0.75:
    score = 2
  else:
    score = 1
  op += sent + ' \t\t' + str(score) + '\n'

print(op)


tokenized_doc = nltk.word_tokenize(doc)
# tag sentences and use nltk's Named Entity Chunker
tagged_sentences = nltk.pos_tag(tokenized_doc)
ne_chunked_sents = nltk.ne_chunk(tagged_sentences)

# extract all named entities

named_entities = []
count = 1
entity_list=""


for tagged_tree in ne_chunked_sents:
    if hasattr(tagged_tree, 'label'):
        entity_name = ' '.join(c[0] for c in tagged_tree.leaves()) #
        entity_type = tagged_tree.label() # get NE category
        named_entities.append((entity_name, entity_type))

named_entities = list(set(named_entities))
# print(named_entities)
for entities in named_entities:
	rep_string = "@entity"+str(count)
	doc = doc.replace(entities[0], rep_string)
	entity_list+="@entity"+str(count)+":"+entities[0]+"\n"
	count+=1

sentences = nltk.sent_tokenize(doc)

# doc+="\n"+entity_list
print(doc)