from rouge import Rouge
import os
import html2text
import nltk
from collections import OrderedDict 
import operator
import html2text
import pycrfsuite
import sys
import time

import crf_train
import crf_test
import k_mix_model_test

FULL_TEXT = '../../FullText_html/'
MANUAL_SUM = '../../CaseAnalysis/'
MAX_LENGTH_SUMMARY = 100 # Define maxmimum words in summary
# MAX_PERCENT_SUMMARY = 34 # 10 # 10 in paper, 34 as discussed
SUMMARY_PERCENT = 34
REACHED_FILE = ''

# 41 min running
##
## Usage: python rouge_crf.py
## Additionally: python rouge_crf.py from_year to_year reached_file
##
## Goes upto, but not including to_year, skips files alphabetically smaller than reached_file
## 

def get_summary(file):
	'''
		Combine crf predictions with k-mix-model
	'''
	text, indices = crf_test.parse_html(file)
	# we have list of sentences and indices, without para information
	doc_length = sum([len(line.split(' ')) for line in text])
	

	tagger = pycrfsuite.Tagger()
	tagger.open('crf_alltrain.model')
	text, X_test, Y_pred = crf_test.test_crf(file, tagger)
	kmm = k_mix_model_test.KMM(file)
	# kmm contains score for each line in text, in serialized order
	kmix_sorted = sorted(kmm.items(), key=operator.itemgetter(1),reverse=True)
	
	# generate_summary
	visited = {}
	summary = {}
	for pair in kmix_sorted:
		sentence_id = pair[0]
		label = Y_pred[sentence_id-1][0]

		if label not in visited:
			summary[text[sentence_id-1]] = label
			visited[label] = 1
		elif visited[label] == 2:
			continue
		else:
			visited[label] = 2
			summary[text[sentence_id-1]] = label

		length = sum([len(key.split(' ')) for key in summary.keys()])
		# print(length, SUMMARY_PERCENT * 0.01 * doc_length)
		if length > SUMMARY_PERCENT * 0.01 * doc_length:
			break


	summary_txt = ''
	order = ['F', 'I', 'A', 'LR', 'SS', 'SP', 'SO', 'R']
	for category in order:
		summary_txt += ''.join([key for key in summary if summary[key]==category]) + '\n'

	# print(summary_txt)
	return summary_txt 



def get_manual_summary(file):
	'''
		Get manual summary from case analysis
	'''
	# rewriting parse_html, as format is different
	with open(file, 'r') as f:
		txt = f.read()
	
	txt=(txt.replace('</?(?!(?:p class=indent)\b)[a-z](?:[^>\"\']|\"[^\"]*\"|\'[^\']*\')*>',''))
	t = html2text.html2text(txt)

	tokenized = nltk.tokenize.sent_tokenize(t)
	t2 = []
	for each in tokenized:
		lines = list( filter( None, each.split('\n') ) )
		t2.extend(lines)

	tokenized = t2
	start = 0 
	
	# Real summary is the first occurence of "Summmary"
	while start < len(tokenized) and 'summary' not in tokenized[start].lower():
		start = start + 1
	
	# 2010_U_113.html has no summary
	if start == len(tokenized):
		return -1

	text = []
	closing = ['appellate history', 'thomson reuters south asia private limited', 'all cases cited',
				'cases citing this case', 'legislation cited']
	
	summary_str = ' **Summary:** '
	text.append(tokenized[start].replace('\n', ' ')[len(summary_str):])

	for i in range(start+1,len(tokenized)):
		if any(closing_phrase in tokenized[i].lower() for closing_phrase in closing) :
			break
		text.append(tokenized[i].replace('\n',' '))
	
	# just in case some closing phrase is missed
	# if('thomson reuters south asia private limited' in tokenized[i].lower()):
	# 	print('verify ', file)
	
	summary = ' '.join(text)
	return summary


def summary_looper(from_year=2010, to_year=2019, reached_file=''):
	'''
		Loop over all files from 2010-2018, generate summaries and compute rouge scores
	'''
	rouge = Rouge()
	scores = OrderedDict()
	summaries = {}
	REACHED_FILE = reached_file
	
	i = sum([ len( os.listdir( FULL_TEXT + str(year) ) ) for year in range(2010, from_year)]) + 1
	i0  = i-1
	# length is total number of documents
	length = sum([ len( os.listdir( FULL_TEXT + str(year) ) ) for year in range(2010, 2019)])
	
	for year in range(from_year, to_year):
		l = sum([len( os.listdir( FULL_TEXT + str(y) ) ) for y in range(from_year, to_year)])
		print('\n\n <=== ', year, ' / ', l, '===>\n\n')
		
		for case in sorted(os.listdir(FULL_TEXT + str(year))):
			print(i, ' / ', length, '=>', case, end='\r')
			if REACHED_FILE != '' and case <= REACHED_FILE:
				i += 1
				continue
			
			i2 = i - i0
			manual_summary = get_manual_summary(MANUAL_SUM   + str(year) + '/' + case)
			if manual_summary == -1:
				print('+- Score ', i2, ' / ', l, '    ', i, ' / ', length, ' ', case, ' => Skipped')
				i += 1
				continue

			start = time.time()
			system_generated_summary = get_summary(FULL_TEXT + str(year) + '/' + case)
			running_time = time.time() - start
			print('Summary generated in ', running_time)

			# available are rouge-1, rouge-2, rouge-l
			scores[case] = rouge.get_scores(system_generated_summary, manual_summary)[0]
			summaries[case] = system_generated_summary
			print('+- Score ', i2, ' / ', l, '    ', i, ' / ', length, ' ', case, ' => ', scores[case])
			i += 1

	# print('\n\n-----------------------------------------')
	# print('Average score for ', len(scores), ' documents')
	# print('Fscore: ', sum([scores[case]['f'] for case in scores])) / len(scores)
	# print('Precision: ', sum([scores[case]['p'] for case in scores])) / len(scores)
	# print('Recall: ', sum([scores[case]['r'] for case in scores])) / len(scores)
	
	# Not doing top 10, instead handpicked cases
	# print('\n Top 10 documents by recall:')
	# metric = {case: scores[case]['r'] for case in scores}
	# sorted_r = sorted(metric.items(), key=operator.itemgetter(1), reverse=True)
	# # printing top 10 rouge scores
	# for i in range(10):
	# 	case = sorted_r[i][0]
	# 	print('# ',i+1, ': ', case, ' => ', sorted_r[i][1])
	# 	print(summaries[case], '\n')


if __name__ == '__main__':
	from_year, to_year, reached_file = 2010, 2019, ''
	if len(sys.argv) > 2:
		from_year, to_year = int(sys.argv[1]), int(sys.argv[2])
	if len(sys.argv) > 3:
		reached_file = sys.argv[3]
	summary_looper(from_year, to_year, reached_file)