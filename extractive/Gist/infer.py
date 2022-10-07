# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 18:11:53 2021

@author: Paheli
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 17:34:18 2021

@author: Paheli
"""
import argparse
from codes import generate_summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default = 'data/text/', type = str, help = 'Folder containing textual data')
    parser.add_argument('--features_path', default = 'data/features/', type = str, help = 'Folder to store features of the textual data')
    parser.add_argument('--summary_path', default = 'data/summaries/', type = str, help = 'Folder to store features of the textual data')

    parser.add_argument('--model_path', default = 'data/summary_model.pkl', type = str, help = 'Path where trained summarization model is present')
    parser.add_argument('--length_file', default = 'data/length.txt', type = str, help = 'Path to file containing summary length')

    args = parser.parse_args()

    
    generate_summary.summary(args)


if __name__ == '__main__':
    main()
        
