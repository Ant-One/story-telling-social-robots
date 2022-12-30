import random
from transformers import pipeline

import sys
import os
import rospy
from qt_robot_interface.srv import *
from std_msgs.msg import String

from enum import Enum

NUMBER_OF_TEXTS = 2
AUTO_SPLIT = True

class sentiment(Enum):
  ANGRY = "anger"
  DISGUSTED = "disgust"
  AFRAID = "fear"
  JOYFUL = "joy"
  NEUTRAL = "neutral"
  SAD = "sadness"
  SURPRISED = "surprise"

def initROS():
  rospy.init_node('story_node')
  rospy.loginfo("story_node started!")
  speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
  gesture_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
  emotion_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=10)

  speech_serv = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
  speech_serv_lips = rospy.ServiceProxy('/qt_robot/behavior/talkText', behavior_talk_text)
  rospy.sleep(3)

  return (speech_pub, gesture_pub, emotion_pub, speech_serv, speech_serv_lips)
  
def showEmotion(emotion, emotion_pub):
  if emotion == sentiment.ANGRY:
    emotion_pub.publish("QT/angry")
  elif emotion == sentiment.DISGUSTED:
    emotion_pub.publish("QT/disgusted")
  elif emotion == sentiment.AFRAID:
    emotion_pub.publish("QT/afraid")
  elif emotion == sentiment.JOYFUL:
    emotion_pub.publish("QT/happy")
  #elif emotion == sentiment.NEUTRAL:
    #emotion_pub.publish("QT/neutral")
  elif emotion == sentiment.SAD:
      emotion_pub.publish("QT/sad")
  elif emotion == sentiment.SURPRISED:
      emotion_pub.publish("QT/surprised")

  rospy.loginfo("showed emotion: " + str(emotion))



def playGesture(gesture, gesture_pub):
  if gesture == sentiment.ANGRY:
    gesture_pub.publish("QT/emotions/angry")
  elif gesture == sentiment.DISGUSTED:
    gesture_pub.publish("QT/emotions/disgusted")
  elif gesture == sentiment.AFRAID:
    gesture_pub.publish("QT/emotions/afraid")
  elif gesture == sentiment.JOYFUL:
    gesture_pub.publish("QT/emotions/happy")
  #elif gesture == sentiment.NEUTRAL:
    #gesture_pub.publish("QT/neutral")
  elif gesture == sentiment.SAD:
    gesture_pub.publish("QT/emotions/sad")
  elif gesture == sentiment.SURPRISED:
    gesture_pub.publish("QT/emotions/surprised")

  rospy.loginfo("played gesture " + str(gesture))
  

def say(text, speech_pub):
  speech_pub.publish(text)
  rospy.loginfo("Said: " + text)

def say_serv(text, speech_serv):
  rospy.loginfo("Speech service saying: " + text)
  rospy.wait_for_service('/qt_robot/speech/say') 
  speech_serv(text)

def say_serv_lips(text, speech_serv):
  rospy.loginfo("Speech service saying with lip-sync: " + text)
  rospy.wait_for_service('/qt_robot/behavior/talkText')
  speech_serv(text)

def splitIntoSentences(text):
  sentences = text.split(".")
  sentences_final = []
  for elem in sentences:
    elem = elem + "."
    elem = elem.strip()
    sentences_final.append(elem)
  del sentences_final[-1]
  return sentences_final

def main():
  (speech_pub, gesture_pub, emotion_pub, speech_serv, speech_serv_lips) = initROS()

  print("QT Robot will tell you a story. Which one do you want to hear?\n")
  textfiles = {}
  with os.scandir('stories/') as entries:
    i = 1
    for entry in entries:
      print(str(i) + " - " + entry.name)
      textfiles[i] = entry.name
      i+=1

  print("Your choice : ")
  choice = int(input())
  with open("stories/" + textfiles.get(choice)) as f:
    text = f.read()

  if AUTO_SPLIT == True:
    splitted = splitIntoSentences(text)
  else:
    splitted = text

  classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base") #return_all_scores=True to return all sentiments

  sentences_with_sentiment = {}

  for element in splitted:
    sentences_with_sentiment[element] = classifier(element)[0].get("label")

  #Now we have a dictionnary with sentences and the related sentiment

  last_sentiment = ()
  for sentence in sentences_with_sentiment.keys():
    if sentiment(sentences_with_sentiment[sentence]) != sentiment.NEUTRAL :
      if sentiment(sentences_with_sentiment[sentence]) != last_sentiment:
        last_sentiment = sentiment(sentences_with_sentiment[sentence])
        print("SENTIMENT -> " + sentences_with_sentiment[sentence])
        showEmotion(sentiment(sentences_with_sentiment[sentence]), emotion_pub)
        playGesture(sentiment(sentences_with_sentiment[sentence]), gesture_pub)
        say_serv(sentence, speech_serv)
      else:
        print("same as before -> speaking with lips")
        say_serv_lips(sentence, speech_serv_lips)
        last_sentiment = sentiment.NEUTRAL
    else:
      print("neutral -> speaking with lips")
      say_serv_lips(sentence, speech_serv_lips)
      last_sentiment = sentiment.NEUTRAL
    rospy.sleep(0.1)
    print("\n")
    

if __name__ == "__main__":
    main()