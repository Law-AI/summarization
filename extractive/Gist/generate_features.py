# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 17:34:18 2021

@author: Paheli
"""
import argparse
from codes import generate_features

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default = 'data/text/', type = str, help = 'Folder containing textual data')
    parser.add_argument('--features_path', default = 'data/features/', type = str, help = 'Folder to store features of the textual data')
    parser.add_argument('--important_words', default = 'data/important_words.txt', type = str, help = 'Text file containing important/domain specific words')
    parser.add_argument('--pos_tags', default = 'data/postags.txt', type = str, help = 'Text file containing relevant pos tags for the task')
    parser.add_argument('--w2v', default = False, type = bool, help = 'Whether to train a word2vec model (on the train data)')
    parser.add_argument('--word2vec_path', default = 'data/word2vec_model.bin', type = str, help = 'Path where pretrained word2vec is present')
    

    args = parser.parse_args()

    print('Generating features for data in  ...'+args.data_path, end = ' ')
    generate_features.features(args)
    
    
if __name__ == '__main__':
    main()
        
