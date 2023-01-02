from enum import Enum

from transformers import pipeline

class sentiment(Enum):
  ANGRY = "anger"
  DISGUSTED = "disgust"
  AFRAID = "fear"
  JOYFUL = "joy"
  NEUTRAL = "neutral"
  SAD = "sadness"
  SURPRISED = "surprise"

class Classifier:
  def __init__(self) -> None:
    self.model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True) #return_all_scores=True to return all sentiments

  def classify(self, text, auto_split):
    if auto_split == True:
      splitted = self.splitIntoSentences(text)
    else:
      splitted = text

    sentences_with_sentiment = {}

    for element in splitted:
      sentences_with_sentiment[element] = self.model(element)
    #Now we have a dictionnary with sentences and the related sentiments

    return sentences_with_sentiment


  def splitIntoSentences(self, text):
    sentences = text.split(".")
    sentences_final = []
    for elem in sentences:
      elem = elem + "."
      elem = elem.strip()
      sentences_final.append(elem)
    del sentences_final[-1]
    return sentences_final
