# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:11:24 2020

@author: Paheli
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:44:29 2020

@author: Paheli
"""
from gensim.models import Word2Vec
import numpy as np
from nltk import word_tokenize
from tqdm import tqdm
import os

def run_code(model_path,data_folder,features_folder):

    model = Word2Vec.load(model_path)
    if not os.path.exists(features_folder):
        os.mkdir(features_folder)
        
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
            words = word_tokenize(sentence)
            length = 0
            for word in sentence:
                if word in model.wv.vocab:
                    vec = model.wv[word]
                    summation = np.add(summation,vec)
                    length+=1
                    
            if length > 0 : summation = summation/length
            summation = np.around(summation,decimals=4)
            fw.write(" ".join(map(str, summation))+"\n")
        
        fw.close()
            
