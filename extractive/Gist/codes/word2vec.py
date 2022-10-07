import os
from nltk import word_tokenize
from gensim.models import Word2Vec
import numpy as np
import string
from tqdm import tqdm

def train_word2vec(train_data_path,save_model_path):
    sentences = []
    print("reading files for word2vec")
    for file in tqdm(os.listdir(train_data_path)):
        fr = open(os.path.join(train_data_path,file),"r")
        for line in fr.readlines():
            line = line.rstrip("\n")
            line = (line.split("$$$")[0]).lstrip(" ").rstrip(" ")
            line = line.translate(str.maketrans('', '', string.punctuation))
            sentences.append(word_tokenize(line))
        

        
    print ("starting word2vec training")
    model = Word2Vec(sentences, min_count=5)
    model.save(save_model_path+"word2vec_model.bin")
    # fw = open(save_model_path+"word-embs.txt","w")
    # for w in list(model.wv.vocab):
    #     fw.write(w+" ")
    #     vec = model.wv[w]
    #     fw.write(" ".join(map(str, vec))+"\n")
    
    # fw.close()
    
    


    
        



    