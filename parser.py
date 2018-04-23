#!/usr/bin/env python3

import sys
from StanfordSentiment import utils
from stanfordcorenlp import StanfordCoreNLP
import json

#read input
inFile = open(sys.argv[1],'r')

correctSentiment = int(sys.argv[2]) #positive = 3, neutral = 2, or negative = 1

stanfordCorrect = 0
newCorrect = 0
total = 0

for line in inFile.readlines():
	print(line)
	total += 1
	#get Stanford annotations
	nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')
	props = {'annotators': 'sentiment,pos','pipelineLanguage':'en','outputFormat':'json'}
	output = json.loads(nlp.annotate(line,properties=props))

	#get Stanford sentiment (takes the average sentiment of all sentences)
	sentiment = 0
	for i in range(len(output['sentences'])):
		sentiment += int(output['sentences'][i]['sentimentValue'])
		#print sentiment
	sentiment = int(round(float(sentiment)/float(len(output['sentences']))))
	if sentiment == correctSentiment:
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