# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:29:28 2020

@author: Paheli
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:35:13 2020

@author: Paheli
"""
import os
from tqdm import tqdm

def run_code(data_folder,sent_pos_folder):
    #data_folder = "F:\\Summarization\\ChineseGist\\NEW SETUP\\test_processed\\processed\\"
    #pathw = "F:\\Summarization\\ChineseGist\\NEW SETUP\\sent-pos\\"
    
    for file in tqdm(os.listdir(data_folder)):
        sent_pos = []
        total_lines=0
        total_lines_list = []
        fr = open(os.path.join(data_folder,file),"r")
        fw = open(os.path.join(sent_pos_folder,file),"w")
        
        for line in fr.readlines():
            line = line.rstrip("\n")
            #ls = line.split("$$$")
            sent = line.lstrip(" ").rstrip(" ")
            total_lines+=1
            sent_pos.append(sent)
            total_lines_list.append(total_lines)
            #print(line)
            
        for i in range(0,len(sent_pos)):
            v = total_lines_list[i]
            k = sent_pos[i]
            rel = float(v)/float(total_lines)
            g = float("{:.5f}".format(rel))
            fw.write(k+" $$$ "+ str(v)+ " $$$ " +str(g)+"\n")
        fw.close()
        fr.close()
            