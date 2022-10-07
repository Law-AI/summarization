# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 09:54:03 2020

@author: Paheli
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:19:23 2020

@author: Paheli
"""
import joblib
import pandas as pd
import os
from tqdm import tqdm
import spacy
import string
from sklearn.preprocessing import StandardScaler

nlp = spacy.load('en_core_web_sm')


def count_word(text):
    doc = nlp(text)
    tokens = [t.text for t in doc]
    tokens = [t for t in tokens if len(t.translate(t.maketrans('', '', string.punctuation + string.whitespace))) > 0] # + string.digits
    #print(tokens)
    
    return len(tokens)


def summary(args):
        
    summary_length_file = args.length_file
    test_data_feats = args.features_path
    test_data_text = args.data_path
    
    

    summary_labelled_path = os.path.join(args.features_path+"pred_scores")
    if not os.path.exists(summary_labelled_path):
        os.mkdir(summary_labelled_path)
    
    if not os.path.exists(args.summary_path):
        os.mkdir(args.summary_path)
    
    
    features_a1a2 = test_data_feats+"features_quant\\"
    features_a3 = test_data_feats+"features_impwords\\"
    features_a4 = test_data_feats+"features_wordemb\\"
    features_a5 = test_data_feats+"features_pos\\"
    features_a6 = test_data_feats+"features_openword\\"
    
    
    #for f in tqdm(folds) :
    
    lgbm_pickle = joblib.load(args.model_path)
    
    fr_len = open(args.length_file,"r")
    
    for line in tqdm(fr_len.readlines()):
        line = line.rstrip("\n")
        ls = line.split("\t")
        f = ls[0]
        reqd_length = int(ls[1])
    
        
        f_a1a2 = os.path.join(features_a1a2,f)
        f_a3 = os.path.join(features_a3,f)
        f_a4 = os.path.join(features_a4,f)
        f_a5 = os.path.join(features_a5,f)
        f_a6 = os.path.join(features_a6,f)
    
    
        
        df_a1a2 = pd.read_table(f_a1a2,delimiter=' ',header=None) 
        df_a3 = pd.read_table(f_a3,delimiter=' ',header=None) 
    
        df_a4 = pd.read_table(f_a4,delimiter=' ',header=None)
        df_a5 = pd.read_table(f_a5,delimiter=' ',header=None) 
        
        df_a6 = pd.read_table(f_a6,delimiter=' ',header=None) 
    
    
        
        df_features = pd.concat([df_a1a2,df_a3,df_a4,df_a5,df_a6],axis=1)
        
        sc = StandardScaler()
        df_features = sc.fit_transform(df_features)

        
        fw = open(os.path.join(summary_labelled_path,f),"w")
        ypred=lgbm_pickle.predict_proba(df_features)
        i=-1
        summary_scores = {}
        sentence_pos = {}
        
        fr = open(os.path.join(test_data_text,f),"r")
    
        for line in fr.readlines():
            line = line.rstrip("\n")
            i+=1
            pred = ypred[i]
            sentence_pos[line] = i
            summary_scores[line] = pred[1]

            fw.write(line+"$$$"+str(pred[1])+"\n")
            #if (i==19):
             #   break
        fw.close()
        fr.close()
        
        sort_sum = sorted(summary_scores.items(), key=lambda item: item[1], reverse = True)
        sort_len = sorted(sentence_pos.items(), key=lambda item: item[1], reverse = False)
    
        shortlist = []
        
        
        fw = open(os.path.join(args.summary_path,f),"w")
        length_so_far = 0
        for tup in sort_sum:
            sent = tup[0]
            length = count_word(sent)
            if length_so_far+length>reqd_length:
                break
            else:
                length_so_far+=length
                shortlist.append(sent)
        
        for tup in sort_len:
            sent = tup[0]
            if sent in shortlist:
                fw.write(sent+"\n")
        fw.close()
        print(f,reqd_length,length_so_far)

    fr_len.close()
        
    
