# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 12:16:56 2020

@author: Paheli
"""

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
import numpy as np
from tqdm import tqdm
import nltk
import os

def run_code(postags, data_folder, features_folder):
    
    fr1 = open(postags,"r")
    if not os.path.exists(features_folder):
        os.mkdir(features_folder)
    features = []
    for line in fr1.readlines():
        line = line.rstrip("\n")
        features.append(line)
    
    
    
    for f in tqdm(os.listdir(data_folder)):
        file = os.path.join(data_folder,f)
        fr = open(file,"r")
        fw = open(os.path.join(features_folder,f),"w")
        for sentence in fr.readlines():
            sentence = sentence.rstrip("\n")
            if "$$$" in sentence:
                sls = sentence.split("$$$")
                sentence = sls[0]
            tokens = nltk.word_tokenize(sentence)
            postags = nltk.pos_tag(tokens)
            ptags = np.zeros(35)
            count=0
            if len(postags)>=10:
                for pair in postags[:10]:
                    onehot = np.zeros(35)
                    ptag = pair[1]
                    if ptag in features:
                        index = features.index(ptag)
                        onehot[index] = 1
                        ptags = np.add(ptags,onehot)
                        count+=1
               
            else:
                x = len(postags)
                for pair in postags[:x]:
                    onehot = np.zeros(35)
                    ptag = pair[1]
                    if ptag in features:
                        index = features.index(ptag)
                        onehot[index] = 1
                        ptags = np.add(ptags,onehot)
                        count+=1
            ptags = ptags/count
                
            #print (ptags)
            fw.write(" ".join(map(str, ptags))+"\n")
        
        fw.close()
        
                
