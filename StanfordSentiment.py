#!/usr/bin/env python3

from stanfordcorenlp import StanfordCoreNLP
from pprint import pprint
import json

class utils():

	@staticmethod
	def callAPI(input,task):
		nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')
		props = {'annotators': 'sentiment,pos','pipelineLanguage':'en','outputFormat':'json'}
		return json.loads(nlp.annotate(input,properties=props))

	@staticmethod
	def getStanfordSentiment(input):
		return utils.callAPI(input,'sentiment')['sentences'][0]['sentiment']

pprint(utils.callAPI("I hate you.",'pos'))