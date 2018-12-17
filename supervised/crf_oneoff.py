import nltk
import sklearn
import scipy.stats
import nltk
from nltk import tokenize
import sklearn_crfsuite
from sklearn_crfsuite import metrics
import sys
import json
from saravanan_constants import include_toggled_phrases, include_toggled_pairs
import saravanan_constants
import operator
import pycrfsuite
import numpy as np
from sklearn.metrics import classification_report

# http://www.albertauyeung.com/post/python-sequence-labelling-with-crf/


cue_phrases = saravanan_constants.categorical_phrases
cue_pairs = saravanan_constants.categorical_pairs
# check saravanan's constants	
include_toggled_phrases(cue_phrases)
include_toggled_pairs(cue_pairs)


##
## Approach 2: Add another mode where instead of using cue_phrases, 
## word level match checks for annotation as per json / txt file.
##
## Approach 3: Self detected cue_phrases and pairs
##

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
	score = {}
	for category in cue_pairs:
		score[category] = 0

	for category in cue_phrases:
		score[category] += sum([ 1 for phrase in cue_phrases[category] if phrase in sentence ])

	found_pairs = {}
	for category in cue_pairs:
		for pair_start in cue_pairs[category]:
			found_index = sentence.find(pair_start)
			if found_index == -1:
				continue
		
			# search if matching pair is found
			line_onward = sentence[found_index + len(pair_start) :]
			# increment score if any cue_pair is present, won't increment if multiple pairs found for pair_start
			if any(subsequent_str in line_onward for subsequent_str in cue_pairs[category][pair_start]):
				score[category] += 1
				found_pairs[pair_start] = ','.join([subsequent_str for subsequent_str in cue_pairs[category][pair_start] if subsequent_str in line_onward])

	label = '-'
	## assign a label based on scores
	max_score = max(score.items(), key=operator.itemgetter(1))[1]
	if max_score == 0:
		label = '-'
	else:
		label = max(score.items(), key=operator.itemgetter(1))[0]
	return label


def wordToFeatures(doc, i):
	'''
		document is a sentence, i is the index
	'''
	word = doc[i][0]
	postag = doc[i][1]
	labelling = doc[i][-1]

	## check if this sentence is of any labelling
	if(labelling=='-'):
		sentence = " ".join([ wordpair[0] for wordpair in doc ])
		labelling = matchCues(sentence)

	# Common features for all words
	features = [
		'bias',
		'word.lower=' + word.lower(),
		'word[-3:]=' + word[-3:],
		'word[-2:]=' + word[-2:],
		'word.isupper=%s' % word.isupper(),
		'word.istitle=%s' % word.istitle(),
		'word.isdigit=%s' % word.isdigit(),
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


def sentenceToFeatures(sentence):
	return [wordToFeatures(sentence, i) for i in range(len(sentence))]


def sentenceToLabels(sentence):
	# return [label for token, label in sentence]
	return [label[-1] for label in sentence]


def add_postag(sentences):
	postagged = []
	for i, sentence in enumerate(sentences):
		tokens = [t for t, label in sentence]
		tagged = nltk.pos_tag(tokens)
		postagged.append([(w, pos, label) for (w, label), (word, pos) in zip(sentence, tagged)])

	return postagged


def trainFromAnnotated(file):
	'''
		Given annotated doc, return features training data
	'''
	## expects text only file, without labels
	with open(file, 'r') as f:
		txt = f.readlines()

	if file.split('.')[-1] == 'json':
		tj = json.loads(''.join(txt))
		txt = tj['content']
		t = list(filter(None, txt.split('\n')))
		t = [i.replace('- ', '') for i in t]
		txt = t

	# break paragraphs into sentences
	# t2 = []
	# for sentence in txt:
	# 	t2.extend(nltk.tokenize.sent_tokenize(sentence))
	# txt = t2

	training = []
	for sentence in txt:
		tokens = nltk.tokenize.word_tokenize(sentence)
		labels = wordLevelMatch(tokens)
		if(len(labels) != 0):
			training.append(labels)

	training_postag = add_postag(training)
	X_train = [sentenceToFeatures(sentence) for sentence in training_postag]
	Y_train = [sentenceToLabels(sentence) for sentence in training_postag]

	return X_train, Y_train


def testing_crf_predetermined_cues(test):
	'''
		Crf has been trained, just report results
	'''
	print('Starting tests')
	with open(test, 'r') as f:
		test_txt = f.readlines()

	# break paragraphs into sentences
	# t2 = []
	# for sentence in test_txt:
	# 	t2.extend(nltk.tokenize.sent_tokenize(sentence))
	# test_txt = t2

	test_sentences = []
	for line in test_txt:
		tokens = nltk.tokenize.word_tokenize(line)
		tokenlist = [(token, '-') for token in tokens]

		test_sentences.append(tokenlist)

	test_postag = add_postag(test_sentences)
	X_test = [sentenceToFeatures(sentence) for sentence in test_postag]
	Y_test = [sentenceToLabels(sentence) for sentence in test_postag]

	tagger = pycrfsuite.Tagger()
	tagger.open('crf_predetermined_cues.model')
	Y_pred = [tagger.tag(xseq) for xseq in X_test]

	labels = {'-': 0}
	counter = 1
	for category in cue_phrases:
		labels[category] = counter
		counter += 1
	
	predictions = [labels[tag] for row in Y_pred for tag in row]
	truths = [labels[tag] for row in Y_test for tag in row]
	c = 0
	for p, t in zip(predictions, truths):
		if p+t!=0:
			print(p, t)
			c+=1
	predictions = np.array([labels[tag] for row in Y_pred for tag in row])
	truths = np.array([labels[tag] for row in Y_test for tag in row])
	# print(len(predictions))
	# print(len(truths))
	print(c, 'identified labels')
	# print(predictions)
	print( classification_report(truths, predictions,target_names=list(cue_phrases.keys()) ) )


def train_crf_predetermined_cues(annotated):
	'''
		Carry out training and prediction for original set of cue_phrases
	'''
	X_train, Y_train = trainFromAnnotated(annotated)

	print('Starting training')
	trainer = pycrfsuite.Trainer(verbose=False)
	for xseq, yseq in zip(X_train, Y_train):
		trainer.append(xseq, yseq)

	trainer.set_params({
		'c1': 0.1, # coefficient for L1 penalty

		'c2': 0.01, # coefficient for L2 penalty

		'max_iterations': 200, # maximum number of iterations
		
		'feature.possible_transitions': True # whether to include transitions that are possible, but not observed
	})

	trainer.train('crf_predetermined_cues.model')


if __name__ == '__main__':
	if(len(sys.argv) < 3):
		print('Usage: python crf.py annotated unannotated')
		exit(0)

	train_crf_predetermined_cues(sys.argv[1])
	testing_crf_predetermined_cues(sys.argv[2])