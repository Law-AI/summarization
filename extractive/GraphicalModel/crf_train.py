import nltk
import sklearn
import scipy.stats
import nltk
from nltk import tokenize
import sklearn_crfsuite
from sklearn_crfsuite import metrics
import sys
import json
# from ..formulated_constants import include_toggled_phrases, include_toggled_pairs
import formulated_constants
import operator
import pycrfsuite
import numpy as np
from sklearn.metrics import classification_report
import re
import os
# http://www.albertauyeung.com/post/python-sequence-labelling-with-crf/

TRAIN_FOLDER = '../annotated'

cue_phrases = formulated_constants.categorical_phrases
cue_pairs = formulated_constants.categorical_pairs
# check to include variations in case	
formulated_constants.include_toggled_phrases(cue_phrases)
formulated_constants.include_toggled_pairs(cue_pairs)

category_abbr = {
	"Argument": "A", "Fact": "F", "Issue": "I",
	"Ruling by lower court": "LR", "Ruling by the present court": "R", 
	"Statute": "SS", "Precedent": "SP",
	"Other general standards including customary equitable and other extra-legal considerations": "SO",
}

# keep track of detected label so that we don't have to run this
# multiple times for the same sentence
detected_label = {}

def wordLevelMatch(tokens):
	'''
	 Check for word level match in cue phrases
	'''
	if( len(tokens)==1 ):
		return []
	tokenLabels = list()

	for token in tokens:
		labelled = 0

		for category in cue_phrases.keys():
			if token in cue_phrases[category] and labelled == 0:
				tokenLabels.append((token, category))
				labelled = 1

		if labelled == 0:
			tokenLabels.append((token, '-'))

	return tokenLabels


def matchCues(sentence):
	'''
		check cue phrases and pairs for a match
	'''
	# priority of assignment is order in which it appears in cue_pairs
	sentence = sentence.replace(',', ' ')
	score = {category: 0 for category in cue_pairs}
	words = sentence.split(' ')

	for category in cue_phrases:
		# handle single words separately
		only_words = [phrase for phrase in cue_phrases[category] if len(phrase.split(' '))== 1]
		score[category] += sum([1 for phrase in only_words if phrase in words])

		proper_phrases = [phrase for phrase in cue_phrases[category] if phrase not in only_words]			
		score[category] += sum([ 1 for phrase in proper_phrases if phrase in sentence ])

	# since currently no pairs exist, commenting this block
	# found_pairs = {}
	# for category in cue_pairs:
	# 	for pair_start in cue_pairs[category]:
	# 		found_index = sentence.find(pair_start)
	# 		if found_index == -1:
	# 			continue
		
	# 		# search if matching pair is found
	# 		line_onward = sentence[found_index + len(pair_start) :]
	# 		# increment score if any cue_pair is present, won't increment if multiple pairs found for pair_start
	# 		if any(subsequent_str in line_onward for subsequent_str in cue_pairs[category][pair_start]):
	# 			score[category] += 1
	# 			found_pairs[pair_start] = ','.join([subsequent_str for subsequent_str in cue_pairs[category][pair_start] if subsequent_str in line_onward])

	label = '-'
	## assign a label based on scores
	max_score = max(score.items(), key=operator.itemgetter(1))[1]
	if max_score == 0:
		label = '-'
	else:
		label = max(score.items(), key=operator.itemgetter(1))[0]
	return label


def wordToFeatures(doc, i, paraRelativePosition):
	'''
		document is a sentence, i is the index
	'''
	word = doc[i][0]
	postag = doc[i][1]
	labelling = doc[i][-1]

	## check if this sentence is of any labelling
	if(labelling=='-' or labelling=='?'):
		sentence = " ".join([ wordpair[0] for wordpair in doc ])
		if sentence not in detected_label:
			detected_label[sentence] = matchCues(sentence)
		labelling = detected_label[sentence]

	# Common features for all words
	features = [
		'bias',
		'word.lower=' + word.lower(),
		'word[-3:]=' + word[-3:],
		'word[-2:]=' + word[-2:],
		'word.isupper=%s' % word.isupper(),
		'word.istitle=%s' % word.istitle(),
		'word.isdigit=%s' % word.isdigit(),
		'within_sentence_position=' + str(i),
		'paraRelativePosition=' + str(paraRelativePosition),
		'postag=' + postag,
		'labelling=' + labelling
	]

	# Features for words that are not
	# at the beginning of a document
	if i > 0:
		word1 = doc[i-1][0]
		postag1 = doc[i-1][1]
		features.extend([
			'-1:word.lower=' + word1.lower(),
			'-1:word.istitle=%s' % word1.istitle(),
			'-1:word.isupper=%s' % word1.isupper(),
			'-1:word.isdigit=%s' % word1.isdigit(),
			'-1:postag=' + postag1
		])
	else:
		# Indicate that it is the 'beginning of a document'
		features.append('BOS')

	# Features for words that are not
	# at the end of a document
	if i < len(doc)-1:
		word1 = doc[i+1][0]
		postag1 = doc[i+1][1]
		features.extend([
			'+1:word.lower=' + word1.lower(),
			'+1:word.istitle=%s' % word1.istitle(),
			'+1:word.isupper=%s' % word1.isupper(),
			'+1:word.isdigit=%s' % word1.isdigit(),
			'+1:postag=' + postag1
		])
	else:
		# Indicate that it is the 'end of a document'
		features.append('EOS')

	return features


def sentenceToFeatures(sentence, paraRelativePosition):
	# return word level features for each sentence
	# paraRelativePosition = Position of para / total number of paras
	return [wordToFeatures(sentence, i, paraRelativePosition) for i in range(len(sentence))]


def sentenceToLabels(sentence):
	# only return label trivially for each word of sentence
	return [label[-1] for label in sentence]


def add_postag(sentences):
	postagged = []
	for i, sentence in enumerate(sentences):
		tokens = [t for t, label in sentence]
		tagged = nltk.pos_tag(tokens)
		postagged.append([(w, pos, label) for (w, label), (word, pos) in zip(sentence, tagged)])

	return postagged


def trainFromAnnotatedTxt(file):
	'''
		Read plain txt based files
	'''
	with open(file, 'r') as f:
		txt = f.readlines()
	
	txt = [i for i in txt if i!='\n']
	start = txt.index('<proposition>\n')
	text = '\n'.join(txt[start+1:len(txt)-1])

	t2 = re.split("S[0-9]+ ", text)
	t2 = list(filter(None, t2)) # remove any empty strings
	t2 = [i.rstrip() for i in t2] # remove trailing \n

	training = []
	for i in range(len(t2)):
		sentence  = t2[i]
		# These are individual sentences, not needed to sent_tokenize here 
		tokens = nltk.tokenize.word_tokenize(sentence[1:]) # sentence[0] is the label
		if len(tokens) == 1:
			continue

		label = sentence[0]
		if label == 'FE' or label == 'FI':
			label = 'F'
		labels = [(token, label) for token in tokens]
		training.append(labels)

	training_postag = add_postag(training)
	X_train = [sentenceToFeatures(training_postag[i], (i+1)*1.0/len(t2)) for i in range(len(training_postag))]
	Y_train = [sentenceToLabels(sentence) for sentence in training_postag]

	return X_train, Y_train


def trainFromAnnotatedJson(file):
	'''
		Given annotated json, return features training data
	'''
	## expects text only file, without labels
	with open(file, 'r') as f:
		txt = f.readlines()

	tj = json.loads(''.join(txt))
	plaintxt = tj['content']
	t = list(filter(None, plaintxt.split('\n')))
	
	# Convert dep- endency to dependency
	# t = [i.replace('- ', '') for i in t]
	# txt = t

	# break paragraphs into sentences
	# t2 = []
	# for sentence in txt:
	# 	t2.extend(nltk.tokenize.sent_tokenize(sentence))
	# txt = t2

	training = []
	para_positions = []
	for tagging in tj['annotation']:
		label = category_abbr[ tagging['label'][0] ]
		sentences = list(filter(None, tagging['points'][0]['text'].split('\n')))
		start = tagging['points'][0]['start']
		# first para has 0 newlines before it
		para_position = plaintxt[:start].count('\n') + 1

		for sentence in sentences:
			tokens = nltk.tokenize.word_tokenize(sentence)
			if len(tokens) == 1:
				continue
			labels = [(token, label) for token in tokens]
			training.append(labels)
			para_positions.append(para_position)

	total_paras = plaintxt.count('\n')
	training_postag = add_postag(training)
	X_train = [sentenceToFeatures(training_postag[i], para_positions[i]*1.0/total_paras) for i in range(len(training_postag))]
	Y_train = [sentenceToLabels(sentence) for sentence in training_postag]

	return X_train, Y_train


def train_crf():
	'''
		Carry out training and prediction for original set of cue_phrases
	'''
	trainer = pycrfsuite.Trainer(verbose=False)

	print('Starting training')

	TXTS = [doc for doc in os.listdir(TRAIN_FOLDER) if doc.split('.')[-1] == 'txt']
	i, length = 1, len(TXTS)
	for file in TXTS:
		print('+ Reading file ', i, ' / ', length, '=> ', file)
		X_train, Y_train = trainFromAnnotatedTxt(TRAIN_FOLDER + '/' + file)
		for xseq, yseq in zip(X_train, Y_train):
			trainer.append(xseq, yseq)
		i += 1

	JSONS = [doc for doc in os.listdir(TRAIN_FOLDER) if doc.split('.')[-1] == 'json']
	i, length = 1, len(JSONS)
	for file in JSONS:
		print('+ Reading file ', i, ' / ', length, '=> ', file)
		X_train, Y_train = trainFromAnnotatedJson(TRAIN_FOLDER + '/' + file)
		for xseq, yseq in zip(X_train, Y_train):
			trainer.append(xseq, yseq)
		i += 1

	trainer.set_params({
		'c1': 0.1, # coefficient for L1 penalty

		'c2': 0.01, # coefficient for L2 penalty

		'max_iterations': 200, # maximum number of iterations
		
		'feature.possible_transitions': True # whether to include transitions that are possible, but not observed
	})

	trainer.train('crf_alltrain.model')
	print('Model saved at crf_alltrain.model')

if __name__ == '__main__':
	'''
		Nothing complex, call the MVP
	'''
	train_crf()