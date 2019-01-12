import sys
import os
import math
import html2text
import operator
import itertools
import operator
import nltk
from nltk import tokenize
from nltk.corpus import stopwords, wordnet as wn
import crf_test

# 
# python k-mix-model-test.py ../FullText_html/2010/2010_A_1.html 
# Pg 139 / 207 in thesis
#

stopwords = set(stopwords.words('english'))
# intentionally skipping out quotes here
punctuation = '!#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
for each in punctuation:
	stopwords.add(each)


def accumulate(l):
	'''
		Group By Key
	'''
	it = itertools.groupby(l, operator.itemgetter(0))
	for key, subiter in it:
		yield key, sum(item[1] for item in subiter)


# Don't process <img> tags, just strip them out. Use an indent of 4 spaces 
# and a page that's 80 characters wide.

# 1st Tokenize and form sentence
def tokenizeSentence(fileContent):
    """
    :param fileContent: fileContent is the file content which needs to be summarized
    :return: Returns a list of string(sentences)
    """
    return tokenize.sent_tokenize(fileContent)


# 2nd Case Folding
def caseFolding(line):
    """
    :param line is the input on which case folding needs to be done
    :return: Line with all characters in lower case
    """
    return line.lower()


# 3rd Tokenize and form tokens from sentence
def tokenizeLine(sentence):
    """
    :param sentence: Sentence is the english sentence of the file
    :return: List of tokens
    """
    return tokenize.word_tokenize(sentence)


# 4th Stop Word Removal
def stopWordRemove(tokens):
    """
    :param tokens: List of Tokens
    :return: List of tokens after removing stop words
    """
    # list_tokens = []
    # for token in tokens:
    #     if token not in stopwords:
    #         list_tokens.append(token)
    # return list_tokens
    list_tokens = [token for token in tokens if token not in stopwords]
    return list_tokens


def KMM(eval_file):

	test_sentences, _ = crf_test.parse_html(eval_file)
	t2 = [caseFolding(sentence) for sentence in test_sentences]
	test_sentences = t2

	index, docId = {}, 1

	for sentence in test_sentences:
		sentence = sentence.strip()
		if len(sentence) == 0:
			continue

		tokens = nltk.tokenize.word_tokenize(sentence)
		final_tokens = stopWordRemove(tokens)
		for token in final_tokens:
			if token not in index:
				index[token] = [ (docId, 1) ]
			else:
				last_entry = index[token][-1]
				if last_entry[0] == docId:
					index[token][-1] = (docId, last_entry[1]+1)
				else:
					index[token].append( (docId, 1) )

		docId = docId + 1
	# for key in index:
	# 	getList=index[key]
	# 	index[key]=list(accumulate(getList))

	N, cf, tf, df = 360, 0, 0, 0
	num= math.log(N)/math.log(2)
	kmixresult={}
	sent_id=1

	for sentence in test_sentences:
		pk=0
		myline=tokenizeLine(sentence)
		final_tokens=stopWordRemove(myline)

		for token in final_tokens:
			if token not in index:
				continue
			tokenlist = index[token]
			cf = 0		
			for x,y in tokenlist:
				if x == 1:
					tf = y
					df=len(tokenlist)
					
				cf = cf + y
			#print 'token='+token
			t= cf * 1.0 / N
			#print 't='+str(t)
			idf = num * 1.0 / df if df else 0
			#print 'idf='+str(idf)
			s = ( ( (cf-df) * 1.0) / df ) if df else 0
			#print 's='+str(s)
			r=1
			r = t/s if s else 0
			#print 'r='+str(r)
			pk = (r / (s+1) ) * (s / (s+1) ) + math.pow( (s / (s+1) ), tf)

		#print sentence
		#print pk
		kmixresult[sent_id] = pk
		sent_id = sent_id + 1
		# print(sentence, kmixresult[sent_id-1])

	# for sentence in test_sentences:
	# 	print(sentence)

	# print(len(test_sentences))
	# print(kmixresult)

	# kmix_sorted = sorted(kmixresult.items(), key=operator.itemgetter(1),reverse=True)
	# for key, value in kmix_sorted:
	# 	print(test_sentences[key-1])

	return kmixresult


if __name__ == '__main__':
	if len(sys.argv) > 1:
		file = sys.argv[1]
	else:
		file = input('Input file to compute scores for: ')
	
	KMM(file)