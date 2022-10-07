# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:03:30 2020

@author: Paheli
"""
from gensim.models import Word2Vec
import numpy as np
from nltk import word_tokenize
from tqdm import tqdm
import os

def run_code(model_path, data_folder, features_folder):
    model = Word2Vec.load(model_path)
    if not os.path.exists(features_folder):
        os.mkdir(features_folder)
    #pathr = "F:\\Summarization\\ChineseGist\\NEW SETUP\\TEST\\test_processed\\processed\\"
    #pathw = "F:\\Summarization\\ChineseGist\\NEW SETUP\\features_a6\\"
    
    for f in tqdm(os.listdir(data_folder)):
        file = os.path.join(data_folder,f)
        fr = open(file,"r")
        fw = open(os.path.join(features_folder,f),"w")
        for sentence in fr.readlines():
            sentence = sentence.rstrip("\n")
            if "$$$" in sentence:
                sls = sentence.split("$$$")
                sentence = sls[0]
            summation = np.zeros(100)
            length=0
            tokens = word_tokenize(sentence)
            openwords = tokens[:5]
            for word in openwords:
                if word in model.wv.vocab:
                    vec = model.wv[word]
                    summation = np.add(summation,vec)
                    length+=1
                    
            if length > 0 : summation = summation/length
            summation = np.around(summation,decimals=4)
            fw.write(" ".join(map(str, summation))+"\n")
        
        fw.close()