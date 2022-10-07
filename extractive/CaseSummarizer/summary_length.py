#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 15:41:27 2018

@author: user
"""
import string
import sys
import math
import os

count = 0
path_orig = sys.argv[1]
path_sum = sys.argv[2]
path_w = sys.argv[3]
length = float(sys.argv[4])

for f in os.listdir(path_orig):
	url_orig = os.path.join(path_orig,f)
	url_sum = os.path.join(path_sum,f)
    
   	count+=1
   	print count
    
	fr = open(url_orig,"r")

	doc_length = 0
	for line in fr.readlines():
	    line = line.rstrip("\n")
	    line = line.translate(None,string.punctuation)
	    ls = line.split(" ")
	    doc_length = doc_length+len(ls)

	summ_length = math.floor(length*float(doc_length))
	print doc_length,summ_length


	output = ""
	fr = open(url_sum,"r")
	rem_length = summ_length
	for line in fr.readlines():
	#            line = line.rstrip("\n")
	    line2 = line.translate(None,string.punctuation)
	    ls = line2.split(" ")
	    if len(ls) < rem_length:
		output+=line
		rem_length = rem_length-len(ls)
		#print rem_length
	if len(ls) > rem_length:
	    last = ' '.join(ls[:int(rem_length)])
	    output+=last

	file_w = open(os.path.join(path_w,f),"w")
   	file_w.write(output)
   	file_w.close()