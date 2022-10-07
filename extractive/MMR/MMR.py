from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import spacy,os
import argparse
import re
from tqdm import tqdm
from collections import OrderedDict
import string
import numpy as np
from spacy.lang.en import English
import time
nl = English()
import sys
import pandas as pd

repeat = 5
data = []
doc = []
l3 = []
summary = []
hypothesis = ""
word_count = []
pair_similarity = []
summary_string = []

def count_word(index):
    global doc
    Doc = nl(doc[index])
    tokens = [t.text for t in Doc]
    tokens = [t for t in tokens if len(t.translate(t.maketrans('', '', string.punctuation + string.whitespace))) > 0] # + string.digits
    return len(tokens)

def store_word_count():
    global word_count,doc
    word_count = []
    for i in range(0,len(doc)):
        word_count.append(count_word(i))
        
def maximum(index, toPrint=0):
    global summary, pair_similarity
    length = len(summary)
    if(length!=0):
        max=0
        for i in range(length):
            a=pair_similarity[index][summary[i]]
            if(a>max):
                max=a
            if toPrint:
              print(str(summary[i])+" -> "+str(a))
        return max
    else:
        return 0

def count_sum(summary):
    sum=0
    length = len(summary)
    for i in range(length):
        sum+=count_word(summary[i])
    return sum

def mmr_sorted(lambda_, doc, length):
    global word_count, pair_similarity, summary
    #print('Inside MMR')
    print(length)
    l3 = []
    vectorizer = TfidfVectorizer(smooth_idf=False)
    X = vectorizer.fit_transform(doc)
    y = X.toarray()
    rows = y.shape[0]
    cols = y.shape[1]
    pair_similarity = []
    for i in range(rows):
        max=-1
        pair_similarity.append([])
        for j in range(rows):
            if(j!=i):
                a = np.sum(np.multiply(y[i],y[j]))
                pair_similarity[-1].append(a)
                if(a>max):
                    max=a
            else:
                pair_similarity[-1].append(1)
        l3.append(max)
    store_word_count()
    l = len(doc)  
    count = 0
    last = -1
    summary = []
    summary_word_count = 0
    while(1):
        if (summary_word_count < length):
            max=-1
            for i in range(l):
                a = maximum(i)
                mmrscore = lambda_*l3[i] - (1-lambda_)*a
                if(mmrscore >= max):
                    max = mmrscore
                    ind = i
            summary.append(ind)
            summary_word_count += word_count[ind]
        else:
            #print('Bye')
            break

def listToString():  
    global summary_string, word_count, hypothesis, summary, doc
    summary_string = []
    leng = 0
    for i in summary:
      if doc[i] not in summary_string:
          summary_string.append(doc[i])
          leng += word_count[i]
    hypothesis = "".join(summary_string) 


parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default = 'data/text/', type = str, help = 'Folder containing textual data')
parser.add_argument('--summary_path', default = 'data/summaries/', type = str, help = 'Folder to store features of the textual data')
parser.add_argument('--length_file', default = 'data/length.txt', type = str, help = 'Path to file containing summary length')


args = parser.parse_args()

print('Generating summary in  ...'+args.summary_path)
num_docs = len(os.listdir(args.data_path))

X1 = pd.read_csv(args.length_file, sep="\t", header=None)

for i in tqdm(range(0,num_docs)):
  length1=X1[1][i]
  #length2=X2[1][i]
  doc = []
  with open(os.path.join(args.data_path,X1[0][i]), 'r') as file:
    for x in file:
      if x != '\n':
        doc.append(x)
  lamda=0.6
  #for j in lamda:
  mmr_sorted(lamda,doc,length1)
  listToString()
  f= open(os.path.join(args.summary_path,X1[0][i]),"w+")
  n = f.write(hypothesis)
  f.close()
  hypothesis=""
