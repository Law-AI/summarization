import nltk
import glob
import tqdm
import pdb

for file in tqdm.tqdm(glob.glob('./Test_Again/*.txt')):
  with open(file, 'r') as f:
    text = f.read()
    f.close()
  with open('./Extractive/ref_summ/' + file[13:], 'r') as f:
    summ_sent = f.read()
    f.close()

  sent_text = nltk.sent_tokenize(text)

  summ_word_tokens = nltk.word_tokenize(summ_sent)

  op = ''

  for sent in sent_text:
    tokenized_text = nltk.word_tokenize(sent)
    num_present = [x in summ_word_tokens for x in tokenized_text]
    num_present = sum(num_present * 1)
    # pdb.set_trace()
    if num_present / len(tokenized_text) < 0.25:
      score = 0
    elif num_present / len(tokenized_text) > 0.75:
      score = 2
    else:
      score = 1
    op += sent + ' \t\t' + str(score) + '\n'

  tokenized_doc = nltk.word_tokenize(op)
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
    op = op.replace(entities[0], rep_string)
    summ_sent = summ_sent.replace(entities[0], rep_string)
    entity_list+="@entity"+str(count)+":"+entities[0]+"\n"
    count+=1

  # print(op)
  # break
  op+="\n\n"+summ_sent
  op+="\n\n"+entity_list
  with open('./Extractive/test_annotated_again/' + file[13:], 'w') as f:
    f.write(op)
    f.close()



