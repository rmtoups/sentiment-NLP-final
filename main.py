#!/usr/bin/env python3

import sys
from StanfordSentiment import utils
from stanfordcorenlp import StanfordCoreNLP
import json
import postprocessor

def checkCorrect(guess):
	if correctSentiment == 'pos':
		if guess > 2:
			return True
		else:
			return False
	if correctSentiment == 'neutral':
		if guess == 2:
			return True
		else:
			return False
	if correctSentiment == 'neg':
		if guess < 2:
			return True
		else:
			return False

#read input
inFile = open(sys.argv[1],'r', encoding="latin-1")

#string, pos, neg, or neutral
correctSentiment = sys.argv[2]

if correctSentiment not in "pos neutral neg":
	print("please indicate pos, neutral, or neg")
	sys.exit()


stanfordCorrect = 0
propCorrect = 0
newCorrect = 0
fixedCount = 0
total = 0

fixedErrors = []
introducedErrors = []

nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

outcsv = open(correctSentiment+"-out.csv","w")

fixed = open("fixedErrors_%s.txt" % (correctSentiment),'w')
introduced = open("introducedErrors_%s.txt" % (correctSentiment),'w')
fixed.write("Stanford\tnew\treview text\n")
introduced.write("Stanford\tnew\treview text\n")
for line in inFile.readlines():
	#print(line)
	line = line.replace('.',';')
	print(line)
	total += 1
	#get Stanford annotations
	props = {'annotators': 'sentiment,pos','pipelineLanguage':'en','outputFormat':'json'}
	output = json.loads(nlp.annotate(line,properties=props))

	sentiment = float(output['sentences'][0]['sentimentValue'])

	propSentiment = postprocessor.propSentiment(output)
	newSentiment = postprocessor.fullSentiment(output)

	stanfordCorrect += checkCorrect(sentiment)
	print(sentiment)

	propCorrect += checkCorrect(propSentiment)
	print(propSentiment)

	newCorrect += checkCorrect(newSentiment)
	print(newSentiment)

	if checkCorrect(sentiment) and not checkCorrect(newSentiment):
		introducedErrors.append(line+str(newSentiment))
		introduced.write("%f\t%f\t%s" % (sentiment,newSentiment,line))
	elif checkCorrect(newSentiment) and not checkCorrect(sentiment):
		fixedErrors.append(line)
		fixed.write("%f\t%f\t%s" % (sentiment,newSentiment,line))

	outcsv.write(str(sentiment))
	outcsv.write(",")
	outcsv.write(str(newSentiment))
	outcsv.write("\n")

print("Errors fixed: ")
for line in fixedErrors:
  print(line)

print("Errors introduced: ")
for line in introducedErrors:
  print(line)

print("\nStanford: %i out of %i correct" % (stanfordCorrect,total))
print("Propagation only: %i out of %i correct" % (newCorrect,total))
print("New system: %i out of %i correct\n" % (newCorrect,total))
print("Errors fixed: ",len(fixedErrors))
print("Errors introduced: ",len(introducedErrors))

nlp.close()
outcsv.close()
fixed.close()
introduced.close()


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
