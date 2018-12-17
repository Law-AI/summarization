"""
Use "2004_Text Summarization Branches Out.pdf" for court case segmentation
Approximate mapping for categories:

Decision Data, Introduction, Context, Analysis, Conclusion - No DD in our case
Using Saravanan's cue phrases to detect patterns

Identifying the case 			
Establishing facts of the case 
Arguing the case
History of the case
Arguments
Ratio
Judgement

###
### NOTE: FI => Saravanan mapping depends on annotated text
### 		Cue phrases might have to be modified based on annotation observing the distinct populous n-grams
###			If doing thematic segmentation, pre-compute everything
### !! get it working with json !!
###

FI	Facts Intrinsic		identifying
FE	Facts Extrinsic		identifying
I 	Issue				establishing
A 	Argument			arguments
LR 	Ruling by lower		history
SS 	Statute				ratio
SP 	Precedent			arguing
SO 	General stds		arguments
R 	Ruling				judgement

FI	Facts Intrinsic		Introduction
FE	Facts Extrinsic		Context      (Not Introduction, maybe discarded)
I 	Issue				Introduction   (Not c?)
A 	Argument			Context
LR 	Ruling by lower		Context
SS 	Statute				Analysis
SP 	Precedent			Analysis
SO 	General stds		Analysis
R 	Ruling				Conclusion
"""

###
### To improve: Citation recognition based on Act No
### 			Break sentences into phrases -> nltk.tokenize doesn't work
### 			nor https://stackoverflow.com/a/48187084
###

from collections import OrderedDict
import operator
from prettytable import PrettyTable
import re
import saravanan_constants
from saravanan_constants import include_toggled_phrases, include_toggled_pairs
import json
import sys
from nltk.corpus import stopwords
from math import log 


MAX_LENGTH_SUMMARY = 100 # Define maxmimum words in summary
MAX_PERCENT_SUMMARY = 34 # 10 # 10 in paper, 34 as discussed

summary_division = {'Introduction':10, 'Context':24, 'Analysis':60, 'Conclusion':6, 'Citation': 0}


mapping_to_CRF = {'FI': "identifying",	'FE': "identifying",
				'I': "establishing", 	'A': "arguments",	'LR': "history",
				'SS': "ratio",			'SP': "arguing",	'SO': "arguments",
				'R': "judgement",		'?': -1
		}

'''
F = identify, I: intro, A: Analysis, LR: Context, SS: Analysis, SP:analysis, , SO:analysis , r: Conclusion
'''
mapping_to_letsum = {'FI': "Introduction",	'FE': "Introduction",
					'I': "Introduction",	'A': "Context", 	'LR': "Context",
					'SS': "Analysis",		'SP': "Analysis",	'SO': "Analysis",
					'R': "Conclusion",		'?': -1
		} # ? to be assigned above category

crf_to_letsum = {"identifying": "Introduction",	"establishing": "Introduction",
				"arguing": "Analysis",			"history": "Context",
				"arguments": "Analysis",		"ratio": "Analysis",
				"judgement": "Conclusion"
		}

####
# selection is for summary, based on:
# 1. position of para in doc
# 2. position of para. in thematic segment
# 3. position of sentence in paragraph
# 4. tf-idf (position of word in document and corpus)
####

# Carry out thematic segmentation first
# filtering to eliminate unimportant quotations and noises
# selection of the candidate units
# production of table style summary <= Not relevant, only restrict limit, proper grammer

cue_phrases = saravanan_constants.categorical_phrases
cue_pairs = saravanan_constants.categorical_pairs

def Mod_LetSum(t):
	'''
		receives a list of sentences, produce categories for each of them
	'''
	label = OrderedDict()
	scores = OrderedDict()
	lines = {}

	# break sentences to phrases
	# for line in t:
	# 	print(line)
	length = sum([ len(line.split(' ')) for line in t ])
	print('+++--- Length of document: ', length)
	print('\n+++--- Printing lines and detected cues\n')

	for line in t:
		score = {'Introduction':0, 'Context':0, 'Analysis':0, 'Conclusion':0, 'Citation': 0}
		lines[line] = [i.lower() for i in line.split(' ')]
		words = lines[line]

		## need to use citation only for phrases, not sentences
		# remove phrase level citations
		## none mapping to citations, rules will be formulated differently

		# print('>', line)
		# print('>>', words)
		# print('\n\n\n')
		# continue

		## check for matching phrases
		found_phrases = []
		for sarav_category in crf_to_letsum:
			letsum_category = crf_to_letsum[sarav_category]
			# print('letsum_category', letsum_category, sarav_category)
			score[letsum_category] += sum([ 1 for i in cue_phrases[sarav_category] if i in line])
			found_phrases.extend([i for i in cue_phrases[sarav_category] if i in line])

		## print line, detected match, and score
		print(line)
		if found_phrases:
			print(found_phrases)
			print('>', score)
		# print('\n')

		## check for matching pairs
		found_pairs = {}
		for sarav_category in crf_to_letsum:
			letsum_category = crf_to_letsum[sarav_category]
			for pair_start in cue_pairs[sarav_category]:
				found_index = line.find(pair_start)
				if found_index == -1:
					continue
				# search if matching pair is found
				line_onward = line[found_index + len(pair_start) :]
				# increment score if any cue_pair is present, won't increment if multiple pairs found for pair_start
				if any(subsequent_str in line_onward for subsequent_str in cue_pairs[sarav_category][pair_start]):
					score[letsum_category] += 1
					found_pairs[pair_start] = ','.join([subsequent_str for subsequent_str in cue_pairs[sarav_category][pair_start] if subsequent_str in line_onward])

		if found_pairs:
			print(found_pairs)
			print('>>', score)
		print('\n')

		# assign labels based on scores
		if score['Citation'] != 0:
			label[line] = 'Citation'
		else:	# maximal score entity
			if max(score.items(), key=operator.itemgetter(1))[1] == 0:
				label[line] = 'Context (d)'
			else:
				label[line] = max(score.items(), key=operator.itemgetter(1))[0]
		scores[line] = score

	print('\n+++--- Printing label assignment \n')
	pt = PrettyTable()
	pt.field_names = ['#', 'Sentence', 'Intro', 'Context', 'Analysis', 'Conclusion', 'Citation', 'Label']
	c = 0
	for line in t:
		score = scores[line]
		for letsum_category in score:
			if score[letsum_category] == 0:
				score[letsum_category] = '.'
		# print(scores[line]['Introduction'], '\t', scores[line]['Context'], '\t', scores[line]['Analysis'],
			 # '\t', scores[line]['Conclusion'], '\t', scores[line]['Citation'], '\t', label[line])
		pt.add_row([c, line[:50], score['Introduction'], score['Context'], score['Analysis'],
					score['Conclusion'], score['Citation'], label[line]])
		c += 1
	
	print(pt)

	### producing summary now
	## carry out thematic segmentation
	## dependent on breaking down phrases of sentence, so stuck
	## currently only using tf-idf
	print('\n+++--- Printing classwise text\n')
	category_txt = {'Introduction':'', 'Context':'', 'Analysis':'', 'Conclusion':'', 'Citation': ''}
	for line in scores:
		if label[line] == 'Context (d)':
			category_txt['Context'] += line
		else:
			category_txt[label[line]] += line

	for category in category_txt:
		print('\n\n', category,'\n\n')
		print(category_txt[category])

	# compute tf-idf scores
	# Following percentage approach for now

	txt = ''.join(t)
	stop_words = list( set( stopwords.words('english') ) )
	summary = OrderedDict({'Introduction':'', 'Context':'', 'Citation': '', 'Analysis':'', 'Conclusion':''})
	
	for category in category_txt:
		specific_txt = category_txt[category]
		words = list( filter(None, specific_txt.split(' ') ) )
		
		words_in_summary = int( (MAX_PERCENT_SUMMARY * length * summary_division[category]) / (100 * 100) )
		# computing within category because order within category matters
		print('To choose', words_in_summary, ' out of ', len(words), ' words for category', category)
		tf_idf = OrderedDict()

		if words_in_summary >= len(words):
			summary[category] = specific_txt
			continue

		for word in words:
			if word in tf_idf:
				continue
			if word.lower() in stop_words:
				tf_idf[word] = 0
				continue
			tf = txt.lower().count( word.lower() )
			di = sum([1 for i in t if word.lower() in i.lower()]) # number of sentences with the word
			di = di if di!= 0 else 0.5 # not really possible, but account for every possibility
			idf = log( len(t) / di ) 
			tf_idf[word] = tf * idf

		tf_idf_scores = [tf_idf[word] for word in tf_idf]
		tf_idf_scores.sort()
		threshold = tf_idf_scores[words_in_summary - 1] # words with a score above this used in summary
		print('Threshold', threshold)
		words_added = 0
		for word in words:
			if tf_idf[word] > threshold:
				summary[category] += word + ' '
				words_added += 1

			# if multiple words have same score, use order of appearance for deciding
			if words_added == words_in_summary:
				break

	print('\n+++--- Printing selected sumamry for each category\n')
	for category in summary:
		print('\n\n', category,'\n\n')
		print(summary[category])




def letsum_loader(file):
	# check saravanan's constants	
	include_toggled_phrases(cue_phrases)
	include_toggled_pairs(cue_pairs)

	with open(file, 'r') as f:
		txt = f.readlines()
	if file.split('.')[-1] == 'json':
		tj = json.loads(''.join(txt))
		txt = tj['content']
		t = list(filter(None, txt.split('\n')))
		t = [i.replace('- ', '') for i in t]
		return t

	text = '\n'.join(txt)
	t2 = re.split("S[0-9]+ ", text)
	t2 = list(filter(None, t2)) # remove any empty strings
	t2 = [i.strip('\n').replace('- ', '') for i in t2]
	t = [i.split(' ') for i in t2]
	t = [' '.join(i[1:]) for i in t]
	# sentences
	# print(t)
	# exit(0)
	# for line in t:
	# 	print(line)

	# labels, original
	# for each in t2:
		# print(each.split(' ')[0])
	return t

if __name__ == '__main__':

	file = "unannotated.txt"
	if len(sys.argv) > 1:
		file = sys.argv[1]

	txt = letsum_loader(file)
	Mod_LetSum(txt)