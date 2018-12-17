import os
from generalize_text import generalize
import json

CATEGORIES_FOLDER = 'categories'
ANNOTATED_FOLDER = 'annotated_json'
CONTENT_FOLDER = 'content_json'
GENERALIZED_FOLDER = 'content_json_generalized'


def iterate_generalize():
	'''
		Extracted categories, then generalized
		Get n-grams for each category
		Then compare
	'''
	categorized_text = {} # key: value => 'Ruling': 'SPACT asds. sd'

	for file in os.listdir(ANNOTATED_FOLDER):
		with open(file, 'r') as f:
			txt = f.readlines()

		tj = json.loads(txt)
		
		




if __name__ == '__main__':
	iterate_generalize()