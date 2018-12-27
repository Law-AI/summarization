
# coding: utf-8

# In[16]:
from __future__ import print_function
import re
from nltk.corpus import stopwords
import nltk
import collections
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import entity2
import numpy as np
import rbm
import math
from operator import itemgetter
import pandas as pd
import sys
from nltk.stem import PorterStemmer
from collections import Counter
import para_reader
import os

porter = PorterStemmer()

stemmer = nltk.stem.porter.PorterStemmer()
WORD = re.compile(r'\w+')


caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

stop = set(stopwords.words('english'))

ratio = 0.34

def split_into_sentences(text):
	text = " " + text + ".  "
	text = text.replace("\n"," ")
	text = re.sub(prefixes,"\\1<prd>",text)
	text = re.sub(websites,"<prd>\\1",text)
	if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
	text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
	text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
	text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
	text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
	text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
	text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
	text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
	if "”" in text: text = text.replace(".”","”.")
	if "\"" in text: text = text.replace(".\"","\".")
	if "!" in text: text = text.replace("!\"","\"!")
	if "?" in text: text = text.replace("?\"","\"?")
	#if "," in text: text = text.replace(",\"","\",")

	text = text.replace(".",".<stop>")
	text = text.replace("?","?<stop>")
	text = text.replace("!","!<stop>")
	#text = text.replace(",","!<stop>")
	text = text.replace("<prd>",".")
	sentences = text.split("<stop>")
	sentences = sentences[:-1]
	sentences = [s.strip() for s in sentences]
	return sentences


# In[20]:
#text = "An army soldier was injured in fierce gun battle with a group of infiltrating terrorists from across the Line of Control in Gali Maidan area of Sawjian sector, while a BSF jawan was injured in unprovoked firing by Pakistani rangers in Hiranagar sector along the international border in Kathua district on Friday.Identifying the injured army soldier as Launce Naik Vinod Kumar and the BSF jawan as Gurnam Singh, sources said that former got injured during an encounter with a group of terrorists who sneaked into Sawjian sector on the Indian side from the Pakistan occupied Kashmir during wee hours of Friday. The encounter was in progress, sources added.Significantly, the infiltration attempt from across the LoC in Sawjian sector of Poonch district came nearly 24 hours after half a dozen heavily armed terrorists attacked a BSF naka along the international border in Kathua district with small arms fire and rocket propelled grenades so as to cross over to the Indian side. The infiltration attempt was foiled by alert BSF personnel who retaliated killing one of them as during illumation of the area with the help of tracer bomb, terrorists fleeing back to Pakistan side were seen carrying a body with them, sources added.Meanwhile, a BSF jawan was injured as Pakistani Rangers continued resorting to mortar shelling and small arms fire on two forward Indian positions at Bobiyan in Hiranagar sector of Kathua district. Sources said that the fire from across the international border first came around 9.35 am and it continued for nearly 40 minutes.Thereafter, the Pakistani Rangers again resumed firing on Indian side around 12.15 noon, sources said, adding that it was continuing till reports last came in. The Indian side was also retaliating.Ever since, India carried out surgical strikes across the Line of Control causing sufficient damage to terrorists and those shielding them last month, Pakistan has been resorting to mortar shelling and small arms fire at one or the other place along the borders in Jammu region. It continued lobbing mortar shells, besides resorting to automatics and small arms fire along the LoC in Rajouri district’s Manjakote area of Bhimber Gali sector throughout Wednesday night.The Indian troops retaliated appropriately. There had been no casualty or damage on the Indian side. Pakistani troops have resorted to firing in Rajouri sector also this afternoon."
#text = "India is my country and I proud to be an Indian. It ranks as the seventh largest country of the world as well as second most populated country of the world. It is also known as Bharat, Hindustan and Aryavart. It is a peninsula means surrounded by oceans from three sides such as Bay of Bengal in east, Arabian Sea in west and Indian Ocean in south. The national animal of India is tiger, national bird is peacock, national flower is lotus and national fruit is mango. The flag of India has tricolor, saffron means purity (the uppermost), white means peace (the middle one having an Ashok Chakra) and green means fertility (the lowest one). Ashok Chakra contains equally divided 24 spokes. The national anthem of India is “Jana Gana Mana”, the national song is “Vande Mataram” and national sport is Hockey.India is a country where people speak many languages and people of different castes, creeds, religions and cultures live together. That’s why India is famous for common saying of “unity in diversity”. It is well known as the land of spirituality, philosophy, science and technology. People of various religions like Hinduism, Buddhism, Jainism, Sikhism, Islam, Christianity and Judaism lives here together from the ancient time. It is famous country for its agriculture and farming which are the backbones of it from the ancient time. It uses it own produced food grains and fruits. It is a famous tourist’s paradise because it attracts people’s mind from all over the world. It is rich in monuments, tombs, churches, historical buildings, temples, museums, scenic beauty, wild life sanctuaries, places of architecture, etc are the source of revenue to it.It is the place where Taj Mahal, Fatehpur Sikri, golden temple, Qutab Minar, Red Fort, Ooty, Nilgiris, Kashmir, Kajuraho, Ajanta and Ellora caves, etc wonders exist. It is the country of great rivers, mountains, valleys, lakes and oceans. The national language of India is Hindi. It is a country where 29 states and UTs. It has 28 states which again have many small villages. It is a chief agricultural country famous for producing sugarcane, cotton, jute, rice, wheat, cereals etc crops. It is a country where great leaders (Shivaji, Gandhiji, Nehru, Dr. Ambedkar, etc), great scientists (Dr. Jagadeeshchandra Bose, Dr Homi Bhabha, Dr. C. V Raman, Dr. Naralikar, etc) and great reformers (Mother Teresa, Pandurangashastri Alhavale, T. N. Sheshan) took birth. It is a country where diversity exists with strong unity and peace."

#text = "Mahatma Gandhi is well known as the “Father of the Nation or Bapu” because of his greatest contributions towards the independence of our country. He was the one who believed in the non-violence and unity of the people and brought spirituality in the Indian politics. He worked hard for the removal of the untouchability in the Indian society, upliftment of the backward classes in India, raised voice to develop villages for social development, inspired Indian people to use swadeshi goods and other social issues. He brought common people in front to participate in the national movement and inspired them to fight for their true freedom.He was one of the persons who converted people’s dream of independence into truth a day through his noble ideals and supreme sacrifices. He is still remembered between us for his great works and major virtues such as non-violence, truth, love and fraternity. He was not born as great but he made himself great through his hard struggles and works. He was highly influenced by the life of the King Harischandra from the play titled as Raja Harischandra. After his schooling, he completed his law degree from England and began his career as a lawyer. He faced many difficulties in his life but continued walking as a great leader.He started many mass movements like Non-cooperation movement in 1920, civil disobedience movement in 1930 and finally the Quit India Movement in 1942 all through the way of independence of India. After lots of struggles and works, independence of India was granted finally by the British Government. He was a very simple person who worked to remove the colour barrier and caste barrier. He also worked hard for removing the untouchability in the Indian society and named untouchables as “Harijan” means the people of God.He was a great social reformer and Indian freedom fighter who died a day after completing his aim of life. He inspired Indian people for the manual labour and said that arrange all the resource ownself for living a simple life and becoming self-dependent. He started weaving cotton clothes through the use of Charakha in order to avoid the use of videshi goods and promote the use of Swadeshi goods among Indians. He was a strong supporter of the agriculture and motivated people to do agriculture works. He was a spiritual man who brought spirituality to the Indian politics. He died in 1948 on 30th of January and his body was cremated at Raj Ghat, New Delhi. 30th of January is celebrated every year as the Martyr Day in India in order to pay homage to him."
#text = "Discipline is something which keeps everyone under good control. It motivates a person to go ahead in the life and get success. Each one of us has experienced discipline in different forms according to their own requirement and understanding towards life. It availability of it in everyone’s life is very necessary to go on the right path. Without discipline life becomes inactive and useless as nothing go according to the plan. If we need to implement our strategy in right way about any project to be completed, we need to be in discipline first. Discipline is generally of two types. One is induced discipline in which we learn to be in discipline by others and another one is self-discipline which comes from own mind to be in discipline. However sometimes, we need motivation from someone effective personality to improve our self-discipline habit.We need discipline in many ways at many stages of our life so it is good to practice discipline from the childhood. Self-discipline means differently to different people such as for students, it means motivating ownself to get concentrated on the study and complete assignments in right time. However, for working person, it means to get up from bed on time in the morning, do exercise to get fit, go to office on time, and do job tasks properly. Self-discipline is highly required by everyone to have, as in modern time no one has time for others to motivate towards being in discipline. Without discipline one can be failure in the life, she/he cannot enjoy academic success or other success in the career. Self-discipline is required in every field like dieting (it needs to control over fatty and junk foods), regular exercise (it needs to concentrate), etc. One can get health disorders and fatty body without control over food so it needs discipline. Parents need to develop self-discipline habits as they need to teach their kids a good discipline. They need to motivate them all time to behave well and do everything at right time. Some naughty children do not follow their parent’s discipline, in such cases parents need to have dare and patience to teach their naughty children. Everyone has different time and capacity to learn the meaning of discipline according to the nature. So, never give up and always try to get in discipline, as a small step can be converted to large step a day."

precision_values = []
recall_values = []
Fscore_values = []
sentenceLengths = []

def remove_stop_words(sentences) :
	tokenized_sentences = []
	for sentence in sentences :
		tokens = []
		split = sentence.lower().split()
		for word in split :
			if word not in stop :
				try :
					tokens.append(porter.stem(word))
				except :
					tokens.append(word)
		
		tokenized_sentences.append(tokens)
	return tokenized_sentences

def remove_stop_words_without_lower(sentences) :
	tokenized_sentences = []
	for sentence in sentences :
		tokens = []
		split = sentence.split()
		for word in split :
			if word.lower() not in stop :
				try :
					tokens.append(word)
				except :
					tokens.append(word)
		
		tokenized_sentences.append(tokens)
	return tokenized_sentences
		

def posTagger(tokenized_sentences) :
	tagged = []
	for sentence in tokenized_sentences :
		tag = nltk.pos_tag(sentence)
		tagged.append(tag)
	return tagged


def tfIsf(tokenized_sentences):
	scores = []
	COUNTS = []
	for sentence in tokenized_sentences :
		counts = collections.Counter(sentence)
		isf = []
		score = 0
		for word in counts.keys() :
			count_word = 1
			for sen in tokenized_sentences :
				for w in sen :
					if word == w :
						count_word += 1
			try:
				score = score + counts[word]*math.log(count_word-1)
			except:
				pass
		try:
			scores.append(score/len(sentence))
		except:
			scores.append(0)
	return scores



def similar(tokens_a, tokens_b) :
	#Using Jaccard similarity to calculate if two sentences are similar
	try:
		ratio = len(set(tokens_a).intersection(tokens_b))/ float(len(set(tokens_a).union(tokens_b)))
		return ratio
	except:
		pass



def similarityScores(tokenized_sentences) :
	scores = []
	for sentence in tokenized_sentences :
		score = 0;
		for sen in tokenized_sentences :
			if sen != sentence :
				score += similar(sentence,sen)
		scores.append(score)
	return scores



def properNounScores(tagged) :
	scores = []
	for i in range(len(tagged)) :
		score = 0
		for j in range(len(tagged[i])) :
			if(tagged[i][j][1]== 'NNP' or tagged[i][j][1]=='NNPS') :
				score += 1
		scores.append(score/float(len(tagged[i])))
	return scores
		

def text_to_vector(text):
	words = WORD.findall(text)
	return collections.Counter(words)


def get_cosine(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])

	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator


def centroidSimilarity(sentences,tfIsfScore) :
	# print("198 ", tfIsfScore)
	if tfIsfScore:
		centroidIndex = tfIsfScore.index(max(tfIsfScore))
	else:
		centroidIndex = 0
	scores = []
	for sentence in sentences :
		vec1 = text_to_vector(sentences[centroidIndex])
		vec2 = text_to_vector(sentence)
		
		score = get_cosine(vec1,vec2)
		scores.append(score)
	return scores


def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


def numericToken(tokenized_sentences):
	scores = []
	for sentence in tokenized_sentences :
		score = 0
		for word in sentence :
			if is_number(word) :
				score +=1 
		scores.append(score/float(len(sentence)))
	return scores


def namedEntityRecog(sentences) :
	counts = []
	for sentence in sentences :
		try:
			count = entity2.ner(sentence)
		except:
			count  = 1
		counts.append(count)
	return counts


def sentencePos(sentences) :
	th = 0.2
	minv = th*len(sentences)
	maxv = th*2*len(sentences)
	pos = []
	for i in range(len(sentences)):
		if i==0 or i==len((sentences)):
			pos.append(0)
		else:
			t = math.cos((i-minv)*((1/maxv)-minv))
			pos.append(t)

	return pos


def sentenceLength(tokenized_sentences) :
	count = []
	maxLength = sys.maxint
	for sentence in tokenized_sentences:
		num_words = 0
		for word in sentence :
				num_words +=1
		if num_words < 3 :
			count.append(0)
		else :
			count.append(num_words)
	
	count = [1.0*x/(maxLength) for x in count]
	return count

def thematicFeature(tokenized_sentences) :
	word_list = []
	for sentence in tokenized_sentences :
		for word in sentence :
			try:
				word = ''.join(e for e in word if e.isalnum())
				#print(word)
				word_list.append(word)
			except Exception as e:
				print("ERR")
	counts = Counter(word_list)
	number_of_words = len(counts)
	most_common = counts.most_common(10)
	thematic_words = []
	for data in most_common :
		thematic_words.append(data[0])
	#print(thematic_words)
	scores = []
	for sentence in tokenized_sentences :
		score = 0
		for word in sentence :
			try:
				word = ''.join(e for e in word if e.isalnum())
				if word in thematic_words :
					score = score + 1
				#print(word)
			except Exception as e:
				print("ERR")
		score = 1.0*score/(number_of_words)
		scores.append(score)
	return scores

def upperCaseFeature(sentences) :
	tokenized_sentences2 = remove_stop_words_without_lower(sentences)
	#print(tokenized_sentences2)
	upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	scores = []
	for sentence in tokenized_sentences2 :
		score = 0
		for word in sentence :
			if word[0] in upper_case :
				score = score + 1
		scores.append(1.0*score/len(sentence))
	return scores

def cuePhraseFeature(sentences) :
	pass

def sentencePosition(paragraphs):
	scores = []
	for para in paragraphs:
		sentences = split_into_sentences(para)
	   # print(len(sentences))
		if len(sentences) == 1 :
			scores.append(1.0)
		elif len(sentences) == 2 :
			scores.append(1.0)
			scores.append(1.0)
		else :
			scores.append(1.0)
			for x in range(len(sentences)-2) :
				scores.append(0.0)
			scores.append(1.0)
	return scores

			
def executeForAFile(filename,output_file_name,cwd) :
	
	os.chdir(cwd+"/"+sys.argv[1])
	file = open(filename, 'r')
	text = file.read()
	text_length = len(text.split(" "))
	try:
		paragraphs = para_reader.show_paragraphs(filename)
	# print(paragraphs)
		#print("Number of paras : %d",len(paragraphs))
		sentences = split_into_sentences(text)
		text_len = len(sentences)
		sentenceLengths.append(text_len)
	except Exception as e:
		print(e,"error 348")
		return
	
	try:
		tokenized_sentences = remove_stop_words(sentences)
		# print(tokenized_sentences)
		tagged = posTagger(remove_stop_words(sentences))
	except Exception as e:
		print(e,"error 355")
		return

	try:
		thematicFeature(tokenized_sentences)
		#print(upperCaseFeature(sentences))
		#print("LENNNNN : ")
		#print(len(sentencePosition(paragraphs)))
	except Exception as e:
		print(e,"error 364")
		return

	try:
		tfIsfScore = tfIsf(tokenized_sentences)
		similarityScore = similarityScores(tokenized_sentences)
	except Exception as e:
		print(e,"error 371")
		return

	try:
		#print("\n\nProper Noun Score : \n")
		properNounScore = properNounScores(tagged)
		#print(properNounScore)
	except Exception as e:
		print(e, "error 379")
		return
	try:
		centroidSimilarityScore = centroidSimilarity(sentences,tfIsfScore)
	except Exception as e:
		print(e)
		print("387")
		sys.exit()
	try:
		numericTokenScore = numericToken(tokenized_sentences)
	except:
		print("392")
		sys.exit()
	try:
		namedEntityRecogScore = namedEntityRecog(sentences)
	except:
		print("397")
		sys.exit()
	try:
		sentencePosScore = sentencePos(sentences)
	except:
		print("402")
		sys.exit()
	try:
		sentenceLengthScore = sentenceLength(tokenized_sentences)
	except:
		print("407")
		sys.exit()
	try:
		thematicFeatureScore = thematicFeature(tokenized_sentences)
		sentenceParaScore = sentencePosition(paragraphs)
	except Exception as e:
		print(e,"error 390")
		sys.exit()

	try:
		featureMatrix = []
		featureMatrix.append(thematicFeatureScore)
		featureMatrix.append(sentencePosScore)
		featureMatrix.append(sentenceLengthScore)
		#featureMatrix.append(sentenceParaScore)
		featureMatrix.append(properNounScore)
		featureMatrix.append(numericTokenScore)
		featureMatrix.append(namedEntityRecogScore)
		featureMatrix.append(tfIsfScore)
		featureMatrix.append(centroidSimilarityScore)
	except Exception as e:
		print(e, "error 405")
		sys.exit()

	try:
		featureMat = np.zeros((len(sentences),8))
		for i in range(8) :
			for j in range(len(sentences)):
				featureMat[j][i] = featureMatrix[i][j]

		#print("\n\n\nPrinting Feature Matrix : ")
		#print(featureMat)
		#print("\n\n\nPrinting Feature Matrix Normed : ")
		#featureMat_normed = featureMat / featureMat.max(axis=0)
		featureMat_normed = featureMat

		feature_sum = []

		for i in range(len(np.sum(featureMat,axis=1))) :
			feature_sum.append(np.sum(featureMat,axis=1)[i])
		print(featureMat_normed)
		#print(featureMat_normed)
		#for i in range(len(sentences)):
		#	print("396 ", featureMat_normed[i])
	except Exception as e:
		print(e , "error 429")
		sys.exit()

	try:
		temp = rbm.test_rbm(dataset = featureMat_normed,learning_rate=0.1, training_epochs=25, batch_size=len(sentences)/7+1,n_chains=len(sentences)-1,
			 n_hidden=8)
	except Exception as e:
		print(e , "error 436")
		print(filename)
		temp = np.ones((len(sentences),8))
		pass

	#print("\n\n")
	#print(np.sum(temp, axis=1))

	try:
		enhanced_feature_sum = []
		enhanced_feature_sum2 = []

		for i in range(len(np.sum(temp,axis=1))) :
			enhanced_feature_sum.append([np.sum(temp,axis=1)[i],i])
			enhanced_feature_sum2.append(np.sum(temp,axis=1)[i])
	except Exception as e:
		print("477 ")
		sys.exit()

	try:
		#print(enhanced_feature_sum)
		#print("\n\n\n")

		enhanced_feature_sum.sort(key=lambda x: x[0])
		#print(enhanced_feature_sum)

		length_to_be_extracted = len(enhanced_feature_sum)/2

	   # print("\n\nThe text is : \n\n")
		#for x in range(len(sentences)):
		 #   print(sentences[x])

		#print("\n\n\nExtracted sentences : \n\n\n")
		extracted_sentences = []
		# print(sentences)
		extracted_sentences.append([sentences[0], 0])
	except:
		print("497")
		pass
	try:
		indeces_extracted = []
		indeces_extracted.append(0)

		for x in range(length_to_be_extracted) :
			if(enhanced_feature_sum[x][1] != 0) :
				extracted_sentences.append([sentences[enhanced_feature_sum[x][1]], enhanced_feature_sum[x][1]])
				indeces_extracted.append(enhanced_feature_sum[x][1])
	except:
		pass

	try:
		extracted_sentences.sort(key=lambda x: x[1])
		# print("517", extracted_sentences)
		finalText = ""
		#print("\n\n\nExtracted Final Text : \n\n\n")
		for i in range(len(extracted_sentences)):
			#print("\n"+extracted_sentences[i][0])
			# print(ratio*text_length, " 522")
			if(len(extracted_sentences[i][0].split(" "))+len(finalText.split(" "))<int(ratio*float(text_length))):
				finalText = finalText + extracted_sentences[i][0]
				# print(finalText)
				continue
			else:
				ind = 0
				# print(extracted_sentences[i][0])
				while len(finalText)<int(ratio*float(text_length)):
					finalText += extracted_sentences[i][0].split(" ")[ind]+" "

	except:
		pass

	try:
		print(len(finalText.split(" "))/float(text_length), "534")
		# sys.exit()
		os.chdir(os.path.join(cwd,sys.argv[2]))
		file = open(output_file_name, "w")
		file.write(finalText)
		file.close()

		os.chdir(cwd)
		file = open("featureSum", "w")
		for item in feature_sum :
			print(item, end = "\n", file = file)

		file = open("enhancedfeatureSum", "w")
		for item in enhanced_feature_sum2 :
			print(item, end = "\n", file = file)
	except Exception as e:
		print(e , "error 497")
		sys.exit()

filename = "article1"
filenames = []
output_file_list = []
cwd = os.getcwd()

for file in os.listdir(os.path.join(cwd,sys.argv[1])):
	filenames.append(file)
	output_file_list.append(file)


for x in range(len(filenames)):
	executeForAFile(filenames[x],output_file_list[x],cwd)
