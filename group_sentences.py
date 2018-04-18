#!/usr/bin/env python3

from stanfordcorenlp import StanfordCoreNLP
import json

nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

sentences_sorted = {}

infile = open("rt-polaritydata/rt-polarity.pos", encoding="latin-1")

for sentence in infile.read().split("\n"):
  if len(sentence)>0:
    result = json.loads(nlp.annotate(sentence, properties={'annotators': 'sentiment','pipelineLanguage':'en','outputFormat':'json'}))['sentences'][0]['sentiment']
    if result not in sentences_sorted:
      sentences_sorted[result] = []
    sentences_sorted[result].append(sentence)

nlp.close()
infile.close()

for sentiment in sentences_sorted:
  outfile = open(sentiment,"w")
  outfile.write("\n".join(sentences_sorted[sentiment]))
  outfile.close()

