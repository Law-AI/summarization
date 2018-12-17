import os
import json

ANNOTATED_FOLDER = 'annotated_json'
CONTENT_FOLDER = 'content_json'

def json_to_content():
	'''
		get content files from each json
	'''
	for file in os.listdir(ANNOTATED_FOLDER):
		with open(ANNOTATED_FOLDER + '/' + file, 'r') as f:
			txt = f.readlines()

		j = json.loads(''.join(txt))

		with open(CONTENT_FOLDER + '/' + ''.join(file.split('.')[:-1]) + '.txt', 'w') as f:
			f.write(j['content'])

		print(file + ' done')


if __name__ == '__main__':
	json_to_content()