# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:22:00 2018

@author: Sounak
"""

import sys
import nltk.data
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import math
import numpy as np
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree
import re
import operator

df_vec = {}
doc_w_vec = {}
total_docs = 0

def cal_df():
    global df_vec
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    path = input_path
    files = os.listdir(path)
    
    for f in files:
        f_path = path + "\\" + f
        #print f_path
        #sys.stdout.flush()
        fp = open(f_path)
        data = fp.read()
        fp.close()
        sntncs = tokenizer.tokenize(data)
    
        # Normalize, remove stop words, lemmatize
        nor_stp_lmt = []
        
        wordnet_lemmatizer = WordNetLemmatizer()
        stop = set(stopwords.words('english'))
        for s in sntncs:
            s_nor_stp_lmt = ""
            s = s.lower()
            words = word_tokenize(s)
            for w in words:
                if w not in stop:
                    w = wordnet_lemmatizer.lemmatize(w).encode('latin1')
                    s_nor_stp_lmt = s_nor_stp_lmt + w + " "
            nor_stp_lmt.append(s_nor_stp_lmt)
        #print nor_stp_lmt
        
        
        # compute TF
        unq_words = {}
        for s in nor_stp_lmt:
            for w in word_tokenize(s):
                if w != ".":
                    if w not in unq_words:
                        unq_words[w] = 0
                    
        
        
        for k in unq_words.keys():
            if k in df_vec:
                df_vec[k] = df_vec[k] + 1
            else:
                df_vec[k] = 1

def cal_total_doc():
    global total_docs
    path = input_path
    files = os.listdir(path)
    total_docs = len(files)

def get_continuous_chunks(text):
     chunked = ne_chunk(pos_tag(word_tokenize(text)))
     continuous_chunk = []
     current_chunk = []
     for i in chunked:
         if type(i) == Tree:
             current_chunk.append(" ".join([token for token, pos in i.leaves()]))
         elif current_chunk:
             named_entity = " ".join(current_chunk)
             if named_entity not in continuous_chunk:
                     continuous_chunk.append(named_entity)
                     current_chunk = []
             else:
                 continue
     return continuous_chunk


legal_words = []

def read_legal_dict():
    l_f = open(dict_path, "r")
    for wd in l_f:
        legal_words.append(wd)
    l_f.close()
    

def cal_tf_Idf():
    global legal_words
    global total_docs
    global doc_w_vec
    global df_vec
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    path = input_path
    files = os.listdir(path)
    
    
    for f in files:
        #print f
        #sys.stdout.flush()
        try:
            tf_idf_sntnc = {}
            f_path = path + "\\" + f
            fp = open(f_path)
            data = fp.read()
            fp.close()
            sntncs = tokenizer.tokenize(data)
        
            # Normalize, remove stop words, lemmatize
            nor_stp_lmt = []
            stp_lmt_cased = []
            wordnet_lemmatizer = WordNetLemmatizer()
            stop = set(stopwords.words('english'))
            for s in sntncs:
                s_nor_stp_lmt = ""
                s_u = s.lower()
                words = word_tokenize(s_u)
                for w in words:
                    if w not in stop:
                        w = wordnet_lemmatizer.lemmatize(w).encode('latin1')
                        s_nor_stp_lmt = s_nor_stp_lmt + w + " "
                nor_stp_lmt.append(s_nor_stp_lmt)
                
                words = word_tokenize(s)
                case_sntnc = ""
                for w in words:
                    if w not in stop:
                        w = wordnet_lemmatizer.lemmatize(w).encode('latin1')
                        case_sntnc = case_sntnc + w + " "
                stp_lmt_cased.append(case_sntnc)
                
            
            
            # compute TF
            tf_vec = {}
            length = 0
            for i in range(len(nor_stp_lmt)):
                s = nor_stp_lmt[i]
                for w in word_tokenize(s):
                    if w != ".":
                        length = length + 1
                        if w in tf_vec:
                            tf_vec[w] = tf_vec[w] + 1
                        else:
                            tf_vec[w] = 1
            # normalize tf
            tf_idf_doc = {}
            for k in tf_vec.keys():
                tf_vec[k] = float(tf_vec[k])/float(length)
                tf_idf_doc[k] = tf_vec[k] * math.log10(float(total_docs)/float(df_vec[k]))
            doc_w_vec[fp] = tf_idf_doc
            
            # Calculated tf-idf for each sentence
            std_list = []
            
            for i in range(len(nor_stp_lmt)):
                s = nor_stp_lmt[i]
                ac_s = sntncs[i]
                sm = 0
                no_of_words = len(word_tokenize(s))
                for w in word_tokenize(s):
                    if w in tf_idf_doc.keys():
                        sm = sm + tf_idf_doc[w]
                tf_idf_s = float(sm)/float(no_of_words)
                tf_idf_sntnc[ac_s] = tf_idf_s
                std_list.append(tf_idf_s)
                
            # Calculating STD
            sd = np.std(std_list)
            for i in range(len(nor_stp_lmt)):
                cased_s = stp_lmt_cased[i]
                ne_list = get_continuous_chunks(cased_s)
                ac_s = sntncs[i]
                e = float(len(ne_list))/float(len(word_tokenize(nor_stp_lmt[i])))
                op = any(char.isdigit() for char in s)
                d = 0
                if op:
                    d = 1
                words = word_tokenize(nor_stp_lmt[i])
                bag = []
                for wd in words:
                    try:
                        wd = wd.replace("[","").replace("]","").replace("(","").replace(")","").replace("{","").replace("}","")
                        r = re.compile(wd + ".*")
                    except:
                        print wd
                    newlist = list(filter(r.match, legal_words))
                    for item in newlist:
                        if item in nor_stp_lmt[i]:
                            bag.extend(item.split(" "))
                myset = set(bag)
                g = float(len(myset))/float(len(words))
                
                tf_idf_sntnc[ac_s] = tf_idf_sntnc[ac_s] + sd*(0.2 * d + 0.3 * e + 1.5 * g)
            
            # sort the dictionary and print in a file
            sorted_x = sorted(tf_idf_sntnc.items(), key=operator.itemgetter(1), reverse=True)
            file_nm = os.path.join(output_path,f)
            w_f = open(file_nm , "w")
            sumr = ""
            for pair in sorted_x:
                sumr = sumr + pair[0] + " "
            w_f.write(sumr)
            w_f.close()
        except:
            print f
            #fexcp.write(f+"\n")
            sys.stdout.flush()
         
           

if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    dict_path = sys.argv[3]

    sys.stdout.flush()
    read_legal_dict()
    cal_df()
   
    cal_total_doc()
    cal_tf_Idf() #compute tf-idf, named entities & generates summary
    
            

