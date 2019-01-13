###
### For a given file, return the classification for each
### 
import crf_train
import html2text
import pycrfsuite
import nltk
import sys
# import numpy as np
import operator
# from sklearn.metrics import classification_report


def parse_html(file):
	'''
		Return usable case content, as list
	'''
	with open(file, 'r') as f:
		txt = f.read()

	txt=(txt.replace('</?(?!(?:p class=indent)\b)[a-z](?:[^>\"\']|\"[^\"]*\"|\'[^\']*\')*>',''))
	t = html2text.html2text(txt)

	tokenized = nltk.tokenize.sent_tokenize(t)
	start = 0 

	# The Judgment was delivered by / 'for educational use only'
	while start < len(tokenized) and 'the judgment was delivered by' not in tokenized[start].lower() :
		start = start + 1

	if start == len(tokenized):
		start = 0
		while 'for educational use only' not in tokenized[start].lower():
			start = start + 1

	text, indices = [], []
	for i in range(start+1,len(tokenized)):
		if 'thomson reuters south asia private limited' in tokenized[i].lower():
			break
		text.append(tokenized[i].replace('\n',' '))
		indices.append(i-start)

	return text, indices


def test_crf(file, tagbot = None):
	'''
		Use pre trained model (crf_alltrain) to classify file
	'''
	text, indices = parse_html(file)
	length = len(indices)
	test_sentences = []
	for line in text:
		tokens = nltk.tokenize.word_tokenize(line)
		labels = [(token, '-') for token in tokens]

		test_sentences.append(labels)

	test_postag = crf_train.add_postag(test_sentences)
	X_test = [crf_train.sentenceToFeatures(test_postag[i], indices[i]*1.0/length) for i in range(len(test_postag))]
	# test is not known at all
	# Y_test = [crf_train.sentenceToLabels(sentence) for sentence in test_postag]		

	tagger = tagbot
	if tagger == None:
		tagger = pycrfsuite.Tagger()
		tagger.open('crf_alltrain.model')
	Y_pred = [tagger.tag(xseq) for xseq in X_test]

	# labels = {'-': 0, '?': 0}
	# counter = 1
	# for category in crf_train.cue_phrases:
	# 	labels[category] = counter
	# 	counter += 1
	
	# predictions = [labels[tag] for row in Y_pred for tag in row]
	## Test is not known
	# # truths = [labels[tag] for row in Y_test for tag in row]
	# c = 0
	# for p, t in zip(predictions, truths):
	# 	if p+t!=0:
	# 		print(p, t)
	# 		c+=1
	# # predictions = np.array([labels[tag] for row in Y_pred for tag in row])
	# # truths = np.array([labels[tag] for row in Y_test for tag in row])
	# # # print(len(predictions))
	# # # print(len(truths))
	# # print(c, 'identified labels')
	# # print(predictions)
	# print( classification_report(truths, predictions,target_names=list(crf_train.cue_phrases.keys()) ) )
	
	return text, X_test, Y_pred



if __name__ == '__main__':
	'''
		Nothing complex, call the MVP
	'''
	if len(sys.argv) > 1:
		file = sys.argv[1]
	else:
		file = input('Provide file name to classify: ')
	test_crf(file)