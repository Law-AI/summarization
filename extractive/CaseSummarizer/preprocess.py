# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:50:36 2019

@author: Paheli
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 14:49:13 2018

@author: user
"""
import sys
import re
import os

path_r = sys.argv[1]
path_w = sys.argv[2]
#path_r = "C:\\Users\\Paheli\\Downloads\\temp"
#path_w = "C:\\Users\\Paheli\\Downloads\\temp_proc" 

for f in os.listdir(path_r):
    
    fileName = os.path.join(path_r,f)
    file = open(fileName, 'r')
    
    documents = []
    documents = (file.read()).strip().split("\n");
    file.close()
    
    for i in range(0,len(documents)):
        line = documents[i]
        if line.startswith("1."):
            break
    doc = documents[i:]
    temp = ""
    for eachDocument in doc[:]:
        eachDocument = re.sub(r'(\d\d\d|\d\d|\d)\.\s', ' ', eachDocument)#removes the paragraph lables 1. or 2. etc.
        eachDocument = re.sub(r'(?<=[a-zA-Z])\.(?=\d)', '', eachDocument)#removes dot(.) i.e File No.1063
        eachDocument = re.sub(r'(?<=\d|[a-zA-Z])\.(?=\s[\da-z])', ' ', eachDocument)#to remove the ending dot of abbr
        eachDocument = re.sub(r'(?<=\d|[a-zA-Z])\.(?=\s?[\!\"\#\$\%\&\'\(\)\*\+\,\-\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~])', '', eachDocument)#to remove the ending dot of abbr
        eachDocument = re.sub(r'(?<!\.)[\!\"\#\$\%\&\'\(\)\*\+\,\-\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]', ' ', eachDocument)#removes the other punctuations
        
        temp = temp +''+eachDocument
    documents = []
    temp = temp.replace("  "," ")
    documents = temp.replace(" ","",1)
    
    file_w = open(os.path.join(path_w,f),"w")
    file_w.write(documents)
    file_w.close()