# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:40:16 2020

@author: Paheli
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:57:03 2020

@author: Paheli
"""
import numpy as np
from tqdm import tqdm
import os

def run_code(hcf_features,data_folder,features_folder):
    fr1 = open(hcf_features,"r")
    if not os.path.exists(features_folder):
        os.mkdir(features_folder)
    features = []
    for line in fr1.readlines():
        line = line.rstrip("\n")
        line = line.lower()
        features.append(line)
    
    for f in tqdm(os.listdir(data_folder)):
        file = os.path.join(data_folder,f)
        fr2 = open(file,"r")
        fw = open(os.path.join(features_folder,f),"w")
        
        for sentence in fr2.readlines():
            sentence = sentence.rstrip("\n")
            if "$$$" in sentence:
                sls = sentence.split("$$$")
                sentence = sls[0]
            
            onehot = np.zeros(94)
            for i in range(0,94):
                f = features[i]
                if f.lower() in sentence.lower():
                    onehot[i] = 1
            fw.write(" ".join(map(str, onehot))+"\n")
        
        fw.close()

    