categorical_phrases = dict()
categorical_pairs = dict()

## identifying the case

categorical_phrases['identifying'] = [
'Question for consideration is', 'Questions for consideration are', 'Point for consideration is', 'Points for consideration are',
'Question that arise for consideration is', 'Questions that arise for consideration are', 
	'Point that arise for consideration is', 'Points that arise for consideration are',
'Question for consideration is', 'Questions for consideration are', 'Point for consideration is', 'Points for consideration are',
'Question before us is', 'Questions before us are', 'Point before us is', 'Points before us are',
'We do not find any reasons to interfere with', 'we do not find anything to interfere with', 'we are not in agreement with ',
	' we do not agree with',
'Order under challenge in that', 'this order is under challenge',
]

categorical_pairs['identifying'] = {
	
}

## establishing facts of the case

categorical_phrases['establishing'] = [
'Relevant facts in this case', 'Facts of the case', 'Facts of this case', 'In the fact of this evidence',
'On the basis of established' ,'On the basis of not established', 'On the basis of failed to establish',
'On the basis of proved', 'On the basis of disproved', 'On the basis ofnot proved',
'Court found that', 'lower court found that', 'appellate court found that', 'authority found that',
'We find that', 'We found that', 'this court finds that', 'this court found that', 'this court find that','It was found that',
'We agree with court' 'We agree with lower court', 'We agree with appellate court' ,'We agree with authority',
'Supreme court says', 'court says',
]

categorical_pairs['establishing'] = {
	'If': ['so to be avoided'],
	'We find that': ['if it is presented by', 'if that we', 'in our view'],
	'We found that': ['if it is presented by', 'if that we', 'in our view'],
	'I': ['find', 'found', 'finds', 'do not find', 'does not find', 'did not find'],
	'We': ['find', 'found', 'finds', 'do not find', 'does not find', 'did not find'],
	'This court': ['find', 'found', 'finds', 'do not find', 'does not find', 'did not find'],
}

## arguing the case

categorical_phrases['arguing'] = [
]


arguing_string = ['"', "'", 'v', 'Vs', 'vs', 'sections', 'sec', 'V', 'Sections', 'Sec']
categorical_pairs['arguing'] = {
	'According to Petitioner': arguing_string,
	'According to Respondent': arguing_string,
	'According to Appellant': arguing_string,
	'Petitioner filed affidavit': arguing_string, 'Petitioner filed counter affidavit': arguing_string,
	'Respondent filed affidavit': arguing_string, 'Respondent filed counter affidavit': arguing_string,
	'Appellant filed affidavit': arguing_string, 'Appellant filed counter affidavit': arguing_string,
	'Petitioner contended': arguing_string, 'Petitioner argued': arguing_string,
	'Respondent contended': arguing_string, 'Respondent argued': arguing_string,
	'Appellant contended': arguing_string, 'Appellant argued': arguing_string,
	
}

## history of the case

categorical_phrases['history'] = [
'Petitioner filed against', 'Appeal is filed against', 'Petition is filed against',
'Before the trial court allowed', 'Before the trial court dismissed', 'Before the Appellate court allowed',
	'Before the authority allowed', 'Before the authority dismissed',
]
# other sentences after processing 1,2, 3, 4, 5, 6, 7 labels => Default label is history

categorical_pairs['history'] = {
	
}

## arguments

categorical_phrases['arguments'] = [
'H.C. was of the view', 'H.C held', 'HC was of the view', 'HC held', 'S.C. was of the view', 'S.C held', 'SC was of the view', 'SC held',
	'Privy Council was of the view', 'Privy Council held', 'Privy council was of the view', 'Privy council held',
	'Lower Court was of the view', 'Lower Court held', 'Lower court was of the view', 'Lower court held',
	'Appellate Court was of the view', 'Appellate Court held', 'Appellate court was of the view', 'Appellate court held',
]

years = [str(x) for x in list(range(1900, 2100))]
categorical_pairs['arguments'] = {
	'v': years, 'Vs': years,
	'We find': ['no merits', 'merits'], 'We found': ['no merits', 'merits'],
	'this court finds': ['no merits', 'merits'], 'this court found': ['no merits', 'merits'],

}

## ratio

categorical_phrases['ratio'] = [
'We hold',
'Not valid', 'legally valid', 'legally not valid',
'Statute', 'In view', 'According', 'We are also of view', 'Holding', 'We are of the view that',
]

categorical_pairs['ratio'] = {
	'No provision in' : ['Act', 'statute', 'act'],
	'If': ['maintainable', 'maintained'],
	'We agree with Court': ['in holding that'], 'We agree with court': ['in holding that'],
}

## judgement
categorical_phrases['judgement'] = [
'In the circumstances', 'Under the circumstances', 'order of the court upheld',
'Dismiss', 'dismissed', 'dismissing', 'sustained', 'rejected', 'allowed',
]

categorical_pairs['judgement'] = {
	'consequently the petition': ['allowed', 'dismissed', 'upheld'],
	'consequently the Appeal': ['allowed', 'dismissed', 'upheld'],
	'consequently the Review': ['allowed', 'dismissed', 'upheld'],
	'consequently the Revision': ['allowed', 'dismissed', 'upheld'],
}


def include_toggled_list(l):
	'''
		If list has summary, it should also have Summary
	'''
	l_ = list()
	for item in l:
		first_toggled = item[0].lower() if item[0].isupper() else item[0].upper()
		l_.append(first_toggled + item[1:])
	l += l_
	l = list(set(l))


def include_toggled_dict(d):
	'''
		If dict has summary: x, it should also have Summary: x
	'''
	d_ = dict()
	for key in d:
		first_toggled = key[0].lower() if key[0].isupper() else key[0].upper()
		d_[first_toggled + key[1:]] = d[key]
	# d = {**d, **d_}
	d.update(d_)


def include_toggled_phrases(phrases):
	'''
		Iterator for each category
	'''
	for category in phrases:
		include_toggled_list(phrases[category])


def include_toggled_pairs(pairs):
	'''
		Iterator for each categorical pair
	'''
	total_pairs, c = sum([ len(pairs[category]) for category in pairs ]), 0
	for category in pairs:
		# 'If': ['so be'],
		# to be extended to
		# 'If': ['so be', 'So be'], 'if': ['so be', 'So be']
		
		if category == 'arguing':
			# print('Passing', category)
			for key in pairs[category]:
				pairs[category][key] = list( set( pairs[category][key] ) )
			pass
		# print('Not passing', category)
		for key in pairs[category]:
			# print ( pairs[category][key] )
			include_toggled_list( pairs[category][key] )
			c += 1
			# print(key, " => ", c, "/", total_pairs)

	c = 0
	for category in pairs:
		d2 = {}
		for key in pairs[category]:
			k2 = key[0].upper() if key[0].islower() else key[0].lower()
			d2[k2 + key[1:]] = pairs[category][key]
			c += 1
			# print(key, " => ", c, "/", total_pairs)			
		pairs[category].update(d2)

	# make a set
	for category in pairs:
		for key in pairs[category]:
			pairs[category][key] = list( set( pairs[category][key] ) )