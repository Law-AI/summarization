# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:22:57 2020

@author: Paheli
"""
import string
from nltk import word_tokenize
import os
import numpy as np
from tqdm import tqdm

def feature_chars(sentence):
    chars = 0
    for n in sentence:
        chars+=1
        
    return chars

def feature_words(sentence):
    words = len(word_tokenize(sentence))
    return words

def feature_uniqwords(sentence):
    w = word_tokenize(sentence)
    uniqwords=len(list(dict.fromkeys(w)))
    
    return uniqwords

def feature_position(positions1,positions2,sentence):
    p1 = positions1.get(sentence)
    p2 = positions2.get(sentence)
    return p1,p2
 

def run_code(data_folder,data_folder_sent_pos,features_folder):       
    
    #data_folder_sent_pos= "F:\\Summarization\\ChineseGist\\NEW SETUP\\sent-pos\\"
    #data_folder = "F:\\Summarization\\ChineseGist\\NEW SETUP\\test_processed\\processed\\"
    #pathw = "F:\\Summarization\\ChineseGist\\NEW SETUP\\features_a1a2\\"
    if not os.path.exists(features_folder):
        os.mkdir(features_folder)
        
        
    positions1= {}
    positions2 = {}
    for file in os.listdir(data_folder_sent_pos):
        fr = open(os.path.join(data_folder_sent_pos,file),"r")
        for line in fr.readlines():
            line = line.rstrip("\n")
            if "$$$" in line:
                ls = line.split("$$$")
                sent = ls[0].lstrip(" ").rstrip(" ")
            else:
                sent = line
            #sent = sent.translate(str.maketrans('', '', string.punctuation))
            pos1 = ls[1].lstrip(" ").rstrip(" ")
            pos2 = ls[2].lstrip(" ").rstrip(" ")
            positions1[file+"///"+sent] = pos1
            positions2[file+"///"+sent] = pos2
            
    for file in tqdm(os.listdir(data_folder)):
        f = os.path.join(data_folder,file)       
        fr1 = open(f,"r")
        fw = open(os.path.join(features_folder,file),"w")
        for line in fr1.readlines():
            line = line.rstrip("\n")
            if "$$$" in line:
                ls = line.split("$$$")
                line = ls[0]

            line_orig = line.rstrip(" ")
            line = line.translate(str.maketrans('', '', string.punctuation))
            s1 = int(feature_chars(line))
            s2 = int(feature_words(line))
            s3 = int(feature_uniqwords(line))
            s4, s5 = feature_position(positions1,positions2,file+"///"+line_orig)
        
            sent = [s1,s2,s3,int(s4),float(s5)]
            
            sent = np.array(sent)
            
            sent = [s1,s2,s3,int(s4),float(s5)]
            sent = np.array(sent)
        
            fw.write(" ".join(map(str, sent))+"\n")
        fw.close()
            
        
        
