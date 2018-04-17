#!/usr/bin/env python

from stanfordcorenlp import StanfordCoreNLP
from pprint import pprint
import json


nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')
sentence = raw_input("Please enter a sentence: ")
#print sentence

prop = props={'annotators': 'sentiment','pipelineLanguage':'en','outputFormat':'json'}

output = json.loads(nlp.annotate(sentence,properties=props))

pprint(output)

print output['sentences'][0]['sentiment']
