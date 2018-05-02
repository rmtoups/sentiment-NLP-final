#!/usr/bin/env python3

import sys
from StanfordSentiment import utils
from stanfordcorenlp import StanfordCoreNLP
import json

def checkCorrect(correctSentiment,guess):
	if correctSentiment == 'pos':
		if guess >= 3:
			return True
		else:
			return False
	if correctSentiment == 'neutral':
		if guess == 2:
			return True
		else:
			return False
	if correctSentiment == 'neg':
		if guess <= 1:
			return True
		else:
			return False

#read input
inFile = open(sys.argv[1],'r')

#string, pos, neg, or neutral
correctSentiment = sys.argv[2]#float(sys.argv[2]) #positive = 3 or 4, neutral = 2, or negative = 1 or 0

if correctSentiment not in "pos neutral neg":
	print("please indicate pos, neutral, or neg")
	sys.exit()


stanfordCorrect = 0
newCorrect = 0
total = 0

for line in inFile.readlines():
	#print(line)
	line = line.replace('.',';')
	print(line)
	total += 1
	#get Stanford annotations
	nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')
	props = {'annotators': 'sentiment,pos','pipelineLanguage':'en','outputFormat':'json'}
	output = json.loads(nlp.annotate(line,properties=props))

	sentiment = int(output['sentences'][0]['sentimentValue'])

	if checkCorrect(correctSentiment,sentiment):
		stanfordCorrect += 1
	print(sentiment)

print("\nStanford: %i out of %i correct" % (stanfordCorrect,total))

#find conjunctions


#compute Stanford Value (positive, neutral, or negative)

#identify contrasting conjunctions
	#either:
		#compute sentiment of contrasting clause
		#assign more weight to it
		#calculate final sentiment
	#or:
		#just flip the overall sentiment of the sentence

#compute accuracy