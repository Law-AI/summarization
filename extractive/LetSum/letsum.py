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

import letsum_test

FULL_TEXT = '../../FullText_html/'
MANUAL_SUM = '../../CaseAnalysis/'
MAX_LENGTH_SUMMARY = 100 # Define maxmimum words in summary
# MAX_PERCENT_SUMMARY = 34 # 10 # 10 in paper, 34 as discussed
SUMMARY_PERCENT = 34
REACHED_FILE = ''

## Max time taken so far: 3.87 hours
##
## Usage: python letsum.py
## Additionally: python letsum.py from_year to_year reached_file
##
## Goes upto, but not including to_year, skips files alphabetically smaller than reached_file
## 


# for 2010_B_31
sys.setrecursionlimit(8735 * 2080 + 10)
# reset to 1000

def summary_letsum_looper(from_year=2010, to_year=2019, reached_file=''):
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
			
			manual_summary = letsum_test.get_manual_summary(MANUAL_SUM   + str(year) + '/' + case)
			if manual_summary == -1:
				print('+- Score ', i2, ' / ', l, '    ', i, ' / ', length, ' ', case, ' => Skipped')
				i += 1
				continue

			start = time.time()
			system_generated_summary = letsum_test.LetSum(FULL_TEXT + str(year) + '/' + case)
			running_time = time.time() - start
			print(system_generated_summary)
			print('Summary generated in ', running_time)

			# available are rouge-1, rouge-2, rouge-l
			# print(len(system_generated_summary.split(' ')))
			# print('\nManual\n', len(manual_summary.split(' ')))
			scores[case] = rouge.get_scores(system_generated_summary, manual_summary)[0]
			summaries[case] = system_generated_summary
			print('+- Score ', i2, ' / ', l, '    ', i, ' / ', length, ' ', case, ' => ', scores[case])
			i += 1

	sys.setrecursionlimit(1000) # reset
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
	summary_letsum_looper(from_year, to_year, reached_file)