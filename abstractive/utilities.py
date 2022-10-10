import glob
from nltk import tokenize
import nltk
import transformers
from torch.utils.data import DataLoader, TensorDataset, random_split, RandomSampler, Dataset
import pandas as pd
import numpy as np
import torch.nn.functional as F
import torch

def get_root_path():
    '''
    function to get root path of dataset

    change the path variable to the path of the dataset
    '''
    path = "/home/pahelibhattacharya/Abhayv2/camera_ready/summarization/dataset"
    return path

def get_summary_data(dataset, train):
    '''
    function to get names, documents, and summaries

    change the path variable to the path of the dataset
    '''
    if dataset == "N2":
        path = get_root_path() + '/N2/Full-Text/India'
        all_files = glob.glob(path + "/*.txt")

        data_source = []
        names = []
        for filename in all_files:
            with open(filename, 'r') as f: 
                p = filename.rfind("/")
#                 print(filename[p+1:])
                names.append(filename[p+1:])
                a = f.read()
                data_source.append(a)
        return names, data_source, []
    
    path = get_root_path() + '/Summary-Data-' + dataset + '/' + train + '-data/judgement'
    all_files = glob.glob(path + "/*.txt")
    data_source = []
    names = []
    for filename in all_files:
        with open(filename, 'r') as f:
            p = filename.rfind("/")
            names.append(filename[p+1:])
            a = f.read()
            data_source.append(a)
    path = get_root_path() + '/Summary-Data-' + dataset + '/' + train + '-data/summary'
    all_files = glob.glob(path + "/*.txt")
    data_summary = []
    for filename in all_files:
        with open(filename, 'r') as f: 
            a = f.read()
            l = len(a)
            data_summary.append(a)
            
    return names, data_source, data_summary

def get_summary_data_rhet_train(dataset):
    '''
    function to get names, documents, and summaries for Rhetorical labeled documents - train

    change the path variable to the path of the Rhetorical labeled dataset
    '''
    path = get_root_path() + '/rhet/' + dataset.lower() + '_ft_rhet' # use your path
    all_files = glob.glob(path + "/*.txt")

    data_source = []
    names = []
    for filename in all_files:
        with open(filename, 'r') as f: 
            p = filename.rfind("/")
            names.append(filename[p+1:])
            a = f.read()
            data_source.append(a)

    path = get_root_path() + '/rhet/RhetSumm_Dataset/raw_files/'+ dataset +'/summary' # use your path
    all_files = glob.glob(path + "/*.txt")

    data_summary = {}
    for filename in all_files:
        with open(filename, 'r') as f: 
            p = filename.rfind("/")
            a = f.read()
            l = len(a)
            data_summary[filename[p+1:]] = (a)
    return names, data_source, data_summary

def get_summary_data_rhet_test(dataset):
    '''
    function to get names, documents, and summaries for Rhetorical labeled documents - test

    change the path variable to the path of the Rhetorical labeled dataset
    '''
    path = get_root_path() + '/rhet/RhetSumm_Dataset/rhet/' + dataset + "/" # use your path
    all_files = glob.glob(path + "/*.txt")

    data_source = []
    names = []
    for filename in all_files:
        with open(filename, 'r') as f: 
            p = filename.rfind("/")
#             print(filename[p+1:])
            names.append(filename[p+1:])
            a = f.read()
            data_source.append(a)

    return names, data_source


def get_req_len_dict(dataset, istrain):
    '''
    function to required length data for each summary

    change the path variable to the path to Summary_Length_India.txt/ Summary_Length_Uk.txt file
    '''
    
    if dataset == "N2":
        f = open(get_root_path() + "/N2/Summary_Length_India.txt", "r")
        a = (f.read())
        a = a.split("\n")
        dict_names = {}
        for i in a:
            b = i.split("	")
            dict_names[b[0] + ".txt"] = int(b[1])
        return dict_names 
    
    f = open(get_root_path() + "/Summary-Data-"+ dataset +"/length-file-" + istrain +".txt", "r")
    a = (f.read())
    a = a.split("\n")
    dict_names = {}
    for i in a:
        b = i.split("	")
        try:
            tp = int(b[2])
            dict_names[b[0]] = tp
        except:
            print(b)
    return dict_names  

def split_to_sentences(para):
    sents = nltk.sent_tokenize(para)
    return sents

def nest_sentencesV2(document,chunk_length):
    '''
    function to chunk a document
    input:  document           - Input document
            chunk_length        - chunk length
    output: list of chunks. Each chunk is a list of sentences.
    '''
    nested = []
    sent = []
    length = 0
    for sentence in nltk.sent_tokenize(document):
        length += len(sentence.split(" "))
        if length < chunk_length:
            sent.append(sentence)
        else:
            nested.append(sent)
            sent = []
            sent.append(sentence)
            length = 0
    if len(sent)>0:
        nested.append(sent)
    return nested

def nest_sentencesMV2(document_sents,chunk_length):
    '''
    function to chunk a document
    input:  doc_sents           - Input document sentences
            chunk_length        - chunk length
    output: list of chunks. Each chunk is a list of sentences.
    '''
    nested = []
    sent = []
    length = 0
    #modeified v2
    
    for sentence in document_sents:
        length += len((sentence.split(" ")))
        if length < chunk_length:
            sent.append(sentence)
        else:
            nested.append(sent)
            sent = []
            sent.append(sentence)
            length = 0
    if len(sent)>0:
        nested.append(sent)
    return nested

def nest_sentences(document,chunk_length):
    '''
    function to chunk a document
    input:  document           - Input document
            chunk_length        - chunk length
    output: list of chunks. Each chunk is a string.
    '''
    nested = []
    sent = []
    length = 0
    for sentence in nltk.sent_tokenize(document):
        length += len(sentence.split(" "))
        if length < chunk_length:
            sent.append(sentence)
        else:
            nested.append(" ".join(sent))
            sent = []
            sent.append(sentence)
            length = 0
    if len(sent)>0:
        nested.append(" ".join(sent))
    return nested
  

def nest_sentencesV3(doc_sents,chunk_length, dict_sents_labels):
    '''
    function to first segment the document using rhetorical roles and then chunk if required
    input:  doc_sents           - Input document sentences
            chunk_length        - chunk length
            dict_sents_labels   - dictionary for every sentence and label
    output: list of chunks
    '''
    s = list(set(dict_sents_labels.values()))
#     print(s)
    all_chunks = []
    
    for label in s:
        doc_sents_withlabels = []
        for sent in doc_sents:
            if sent == '':continue
            if dict_sents_labels[sent] == label:
                doc_sents_withlabels.append(sent)
        chunks = nest_sentencesMV2(doc_sents_withlabels, chunk_length)
        
        edited_chunks = []
        for chunk in chunks:
            edited_chunks.append(["<" + label + ">"] + chunk)
        
        all_chunks = all_chunks + edited_chunks

    return all_chunks   

def get_doc_sens_and_labels(doc):
    '''
    Function to read a Rhetorically labeled document.
    returns a list of sentences, the label of each sentence, dictionary: keys-sentences, values-labels
    '''
    sents = []
    labels = []
    dict_sents_labels = {}
    ss = doc.split("\n")
    for i in ss:
        try:
            spt = i.split("\t")
            sents.append(spt[0])
            labels.append(spt[1])
            dict_sents_labels[spt[0]] = spt[1] 
        except:
            pass
    return sents, labels, dict_sents_labels