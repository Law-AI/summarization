import sys
import os
import math
import html2text
import operator
import itertools
import operator
from nltk import tokenize
from nltk.corpus import stopwords, wordnet as wn
import crf_test
# 
# python k-mix-model.py unannotated-text.txt
# Pg 139 / 207 in thesis
#

KMM_TRAIN_FOLDER = '../kmix_train'
# KMM_TRAIN_FOLDER = '../FullText_html/'

stopword_set = set(stopwords.words('english'))
stopword_set.add('[')

def extractorData(html):
	# dummy list
	start = 0
	tokenized= tokenizeSentence(html)
	# The Judgment was delivered by / 'for educational use only'
	while 'the judgment was delivered by' not in tokenized[start].lower() \
		and 'for educational use only' not in tokenized[start].lower():
		start = start + 1
	ans=[]
	for i in range(start+1, len(tokenized)):
		if 'thomson reuters' in tokenized[i]:
			break
		ans.append(tokenized[i])
	return ans


def accumulate(l):
	'''
		Group By Key
	'''
	it = itertools.groupby(l, operator.itemgetter(0))
	for key, subiter in it:
		yield key, sum(item[1] for item in subiter)


def find_nth(haystack, needle, n):
	start = haystack.find(needle)
	while start >= 0 and n > 1:
		start = haystack.find(needle, start+len(needle))
		n -= 1
	return start

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
    list_tokens = []
    for token in tokens:
        if (token not in stopword_set) and (token != '.') and (token != ','):
            list_tokens.append(token)
    return list_tokens

def KMM(eval_file):

	training =  os.listdir(KMM_TRAIN_FOLDER)
	listOfData=[]
	maxof=0
	nameof=None

	for file in training:
		with open('./'+KMM_TRAIN_FOLDER+'/'+file, 'r') as f:
			txt = f.read()

		txt=(txt.replace('</?(?!(?:p class=indent)\b)[a-z](?:[^>\"\']|\"[^\"]*\"|\'[^\']*\')*>',''))
		if(len(txt)>maxof):
			maxof=len(txt)
			nameof=file

		converted_text = html2text.html2text(txt)
		listOfData.append(caseFolding(converted_text))

	# print(nameof, '\n', maxof)

	with open(eval_file, 'r') as f:
		mysentences = f.readlines()
	# mysentences, _ = crf_test.parse_html(eval_file)

	mysentences_id=None
	idx=1

	t2 = [caseFolding(sentence) for sentence in mysentences]
	mysentences = t2

	index={}
	listOfSentences=[]
	docId=1
	startReading=False


	for file in listOfData:
		sentences = extractorData(file)
		
		for sentence in sentences:
			sentence=sentence.strip()
			if len(sentence)==0:
				continue
			else:
				tokens=tokenizeLine(sentence)
				final_tokens=stopWordRemove(tokens)
				for token in final_tokens:
					if token not in index:
						index[token]= []

					index[token].append( (docId, 1) )
		docId=docId+1
	
	for key in index:
		getList=index[key]
		index[key]=list(accumulate(getList))
		if len(getList) > 2:
			print(key, '=>', index[key])
			print(index[key])

	print(len(index))
	N, cf, tf, df = 360, 0, 0, 0
	num= math.log(N)/math.log(2)
	kmixresult={}
	sent_id=1

	for sentence in mysentences:
		pk=0
		myline=tokenizeLine(sentence)
		final_tokens=stopWordRemove(myline)

		for token in final_tokens:
			if token not in index:
				continue
			mylist=index[token]
			cf=0		
			for x,y in mylist:
				if x==1:
					tf=y
					df=len(mylist)
					
				cf=cf+y
			#print 'token='+token
			t= cf*1.0/N
			#print 't='+str(t)
			idf = num*1.0/df if df else 0
			#print 'idf='+str(idf)
			s = (((cf-df)*1.0)/df) if df else 0
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

	# for sentence in mysentences:
	# 	print(sentence)

	# print(len(mysentences))
	# print(kmixresult)
	
	# sorted_d = sorted(kmixresult.items(), key=operator.itemgetter(1),reverse=True)
	return kmixresult
	# oFile = open('k_mix_output.txt', 'w')
	# for key,value in sorted_d:
	# 	oFile.write(str(key)+'\t'+str(value)+'\n')
	# oFile.close()


if __name__ == '__main__':
	if(len(sys.argv) < 2) :
		print('Need to provide file to evaluate!')
		exit(0)
	
	KMM(sys.argv[1])