from stanfordcorenlp import StanfordCoreNLP
import json
from nltk.tree import *

nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

#result = json.loads(nlp.annotate(sentence, properties={'annotators': 'sentiment','pipelineLanguage':'en','outputFormat':'json'}))

def propSentiment(result):
  s = 0
  for sentenceResult in result["sentences"]:
    atree = Tree.fromstring(sentenceResult["sentimentTree"])
    s += propagateSentimentFromTree(atree)
  return s/len(result["sentences"])

def propagateSentimentFromTree(atree):
  if type(atree[0]) is str:
    return int(atree.label().split('|')[1][len("sentiment="):])
  else:
    return sum( [propagateSentimentFromTree(child) for child in atree] ) / len(atree)


def fullSentiment(result):
  s = 0
  for sentenceResult in result["sentences"]:
    atree = Tree.fromstring(sentenceResult["sentimentTree"])
    s += getSentimentFromTree(atree)
  return s/len(result["sentences"])

def getSentimentFromTree(atree):
  if type(atree[0]) is str:
    #if(atree[0] in simpleNegatives):
    #  print("!!! Negation in unrecognized structure !!!")
    #elif(atree[0] in simpleContrasts):
    #  print("!!! Contrast in unrecognized structure !!!")
    return int(atree.label().split('|')[1][len("sentiment="):])
  else:
    return getNegationSentiment(atree, getSentimentFromTree) or getContrastConjunctionSentiment(atree,getSentimentFromTree) or (sum( [getSentimentFromTree(child) for child in atree] ) / len(atree))

simpleNegatives = {"not", "n't", "never"}
simpleContrasts = {"but", "yet"}

def getNegationSentiment(atree, method):
  if atree.label().split('|')[0] == "@VP" and type(atree[1][0]) is str and atree[1][0] in simpleNegatives:
    if len(atree) != 2:
      print("Weird: nonbinary", atree)
    return -2/3 * method(atree[1]) # assuming it only has two children

  return 0

clauseLabels = {"S","@S","SBAR","@SBAR"}

def getContrastConjunctionSentiment(atree, method):
  if atree.label().split('|')[0] in clauseLabels and atree[0].label().split('|')[0] == "@S" and type(atree[0][1].label().split('|')[0]) is str and atree[0][1].label().split('|')[0] in simpleContrasts:
    return method(atree[1]) - method(atree[0][0])/2
  elif len(atree) >= 2 and atree[1].label().split('|')[0] == "SBAR" and type(atree[1][0][0]) is str and atree[1][0][0] in simpleContrasts:
    return method(atree[1][1]) - method(atree[0])/2

  return 0

#def heuristicsWithoutPropagate(result):


# -> normally, propagate sentiments up.
# -> VP (@VP * _neg_) (*) : negate stuff

#(@S (@S * _conj_) *)

