"""
Use "2004_Text Summarization Branches Out.pdf" for court case segmentation
Approximate mapping for categories:

Decision Data, Introduction, Context, Analysis, Conclusion - No DD in our case

FI	Facts Intrinsic		Introduction
FE	Facts Extrinsic		Introduction      (Not Introduction, maybe discarded)
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
###

from collections import OrderedDict
import operator
from prettytable import PrettyTable
import re

mapping = {'FI': "Introduction", 'I': "Introduction",
			'FE': "Introduction", 'A': "Context", 'LR': "Context",
			'SS': "Analysis", 'SP': "Analysis", 'SO': "Analysis",
			'R': "Conclusion", '?': -1
		} # ? to be assigned above category

# letsum fails trivially, as in krishna_raju the sentences in Indian courts are complex.

intro_words = ["application for judicial review", "application to review a decision", "motion filed by", "Statement of claim"]
intro_titles = ["Introduction", "Summary"]
pre_intro_titles = ["Reasons for order","Reasons for judgment and order"]

context_words = ["advise", "indicate", "concern","request"]
# situation past tense, narration form
context_titles = ["Facts", "Background", "Factual background", "Agreed statement of the facts"]

analysis_words = ["I", "we", "this court", "In reviewing the sections no. of the act", "Pursuant to section no.", "as I have stated",
				 "In the present case", "The case at bar is"]
analysis_titles = ["Analysis", "Decision of the court"]

conclusion_words = ["note", "accept", "summarise", "summarize", "scrutinize", "think", "say", "satisfy","discuss",
					"conclude", "find", "believe", "reach", "persuade", "agree", "indicate", "review",
					"opinion", "conclusion", "summary", "because", "cost", "action"]
conclusion_imp_words = ["allow", "deny", "grant", "refuse"]
conclusion_phrases = ["The motion is dismissed", "the application must be granted", "in the case at bar", "for all the above reasons",
					 "in my view", "my review of", "in view of the evidence", "finally", "thus", "consequently", "in the result"]
conclusion_titles = ["Conclusion", "Costs", "Disposition"]

# citations removed
citation_words = ["conclude", "define", "indicate", "provide", "read", "reference", "refer", "say", "state", "summarize",
					"section", "subsection", "Sub-section", "act", "IPC", "I.P.C"]
citation_phrases = ["following", "section", "subsection", "page", "paragraph", "para", "pursuant"]
# remove line after as follows:
# starting with number

####
# selection is for summary, based on:
# 1. position of para in doc
# 2. position of para. in thematic segment
# 3. position of sentence in paragraph
# 4. tf-idf (position of word in document and corpus)
####

# Carry out thematic segmentation first
# filtering toeliminate unimportant quotations and noises
# selection of the candidate units
# production of table style summary

def include_toggled(l):
	'''
		If list has summary, it should also have Summary
	'''
	l_ = list()
	for each in l:
		first_toggled = each[0].lower() if each[0].isupper() else each[0].upper()
		l_.append(first_toggled + each[1:])
	l += l_


def LetSum(t):
	'''
		receives a list of sentences, produce categories for each of them
	'''
	label = OrderedDict()
	scores = OrderedDict()
	lines = {}
	for each in t:
		score = {'intro':0, 'context':0, 'analysis':0, 'conclusion':0, 'citation': 0}
		lines[each] = [i.lower() for i in each.split(' ')]
		words = lines[each]
		# score intro
		score['intro'] 		= sum([ words.count(i) for i in intro_words ])
		score['context'] 	= sum([ words.count(i) for i in context_words ])
		score['analysis']	= sum([ words.count(i) for i in analysis_words ])

		score['conclusion']	= sum([ words.count(i) for i in conclusion_words ])
		score['conclusion']+= sum([ words.count(i) for i in conclusion_phrases ])
		score['conclusion']+= sum([ words.count(i) for i in conclusion_imp_words ]) * 2

		score['citation']	= sum([ words.count(i) for i in citation_words ])
		score['citation']  += sum([ words.count(i) for i in citation_phrases ])

		if score['citation'] != 0:
			label[each] = 'citation'
		else:	# maximal score entity
			if max(score.items(), key=operator.itemgetter(1))[1] == 0:
				label[each] = '?'
			else:
				label[each] = max(score.items(), key=operator.itemgetter(1))[0]
		scores[each] = score

	pt = PrettyTable()
	pt.field_names = ['#', 'Sentence', 'Intro', 'Context', 'Analysis', 'Conclusion', 'Citation', 'Label']
	c = 0
	for each in t:
		# print(scores[each]['intro'], '\t', scores[each]['context'], '\t', scores[each]['analysis'],
			 # '\t', scores[each]['conclusion'], '\t', scores[each]['citation'], '\t', label[each])
		pt.add_row([c, each[:50], scores[each]['intro'], scores[each]['context'], scores[each]['analysis'],
					scores[each]['conclusion'], scores[each]['citation'], label[each]])
		c += 1
	
	print(pt)



if __name__ == '__main__':
	
	include_toggled(intro_words)
	include_toggled(context_words)
	include_toggled(analysis_words)
	include_toggled(conclusion_words)
	include_toggled(conclusion_imp_words)
	include_toggled(conclusion_phrases)
	include_toggled(citation_words)
	include_toggled(citation_phrases)


	file = "unannotated.txt"
	with open(file, 'r') as f:
		txt = f.readlines()
	text = '\n'.join(txt)
	t2 = re.split("S[0-9]+ ", text)
	t2 = list(filter(None, t2)) # remove any empty strings
	t2 = [i.strip('\n') for i in t2]
	t = [i.split(' ') for i in t2]
	t = [' '.join(i[1:]) for i in t]
	# sentences
	for each in t:
		print(each)
	# labels, original
	# for each in t2:
		# print(each.split(' ')[0])
	LetSum(t)