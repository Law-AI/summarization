# python3
import os
import re
from letsum import mapping

ANNOTATED_FOLDER = 'annotated'
CATEGORIES_LS_FOLDER = 'categories_letsum'
def extract_loop():
	'''
		run a loop to get all sentences
		categories - 
	'''
	stmts = {}
	previous_category = ''
	for file in os.listdir(ANNOTATED_FOLDER):
		# print('Working on ', file)
		with open(ANNOTATED_FOLDER + '/' + file, 'r') as f:
			txt = f.readlines()
		txt = [i for i in txt if i!='\n']
		start = txt.index('<proposition>\n')
		
		text = '\n'.join(txt[start+1:len(txt)-1])
		t2 = re.split("S[0-9]+ ", text)
		t2 = list(filter(None, t2)) # remove any empty strings
		for line in t2:
			category_or = line.split(' ')[0]
			category = mapping[category_or]
			if category_or == '?':
				category = previous_category

			if category not in stmts:
				stmts[category] = []
				print(category,' first showed up', category_or)
			stmts[category].append(' '.join(line.split(' ')[1:])) # remove category
			previous_category = category

	print('Categories detected: ', ' '.join(stmts.keys()))

	print('Writing into files now')
	for category in stmts:
		categorized = stmts[category]
		# [:-1] to remove /n
		# categorized = ['<s> ' + i[:-2] + ' </s>' for i in categorized]
		categorized = [ i[:-2] for i in categorized]
		categorytext = '\n'.join(categorized)
		with open(CATEGORIES_LS_FOLDER + '/' + category + '.txt', 'w') as f:
			f.write(categorytext)
		print(category + ' done')

if __name__ == '__main__':
	extract_loop()