# python3
import os
import re
import json

ANNOTATED_FOLDER = 'annotated'
CATEGORIES_FOLDER = 'categories'

category_abbr = {
	"Argument": "A", "Fact": "F", "Issue": "I",
	"Ruling by lower court": "LR", "Ruling by the present court": "R", 
	"Statute": "SS", "Precedent": "SP",
	"Other general standards including customary equitable and other extra-legal considerations": "SO",
}


def extract_loop():
	'''
		run a loop to get all sentences
		categories - 
	'''
	stmts = {}
	for file in [doc for doc in os.listdir(ANNOTATED_FOLDER) if doc.split('.')[-1] == 'txt']
		# print('Working on ', file)
		with open(ANNOTATED_FOLDER + '/' + file, 'r') as f:
			txt = f.readlines()
		txt = [i for i in txt if i!='\n']
		start = txt.index('<proposition>\n')
		
		text = '\n'.join(txt[start+1:len(txt)-1])
		t2 = re.split("S[0-9]+ ", text)
		t2 = list(filter(None, t2)) # remove any empty strings
		for line in t2:
			category = line.split(' ')[0]
			if category == 'FE' or category == 'FI':
				category = 'F'
			if category not in stmts:
				stmts[category] = []
				print(category,' first showed up')
			stmts[category].append(' '.join(line.split(' ')[1:])) # remove category

	# JSONs
	for file in [doc for doc in os.listdir(ANNOTATED_FOLDER) if doc.split('.')[-1] == 'json']
		with open(ANNOTATED_FOLDER + '/' + file, 'r') as f:
			txt = f.readlines()
		tj = json.loads(''.join(txt))

		for tagging in tj['annotation']:
			category = category_abbr[ tagging['label'][0] ]
			sentences = list(filter(None, tagging['points'][0]['text'].split('\n')))
			if category not in stmts:
				stmts[category] = []
				print(category,' first showed up')

			stmts[category].extend(sentences)


	print('Categories detected: ', ' '.join(stmts.keys()))

	print('Writing into files now')
	for category in stmts:
		categorized = stmts[category]
		categorized = [ i.rstrip() for i in categorized]
		categorytext = '\n'.join(categorized)
		with open(CATEGORIES_FOLDER + '/' + category + '.txt', 'w') as f:
			f.write(categorytext)
		print(category + ' done')

if __name__ == '__main__':
	extract_loop()