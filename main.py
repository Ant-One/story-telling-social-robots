import os
import time

#import rospy

#from robot_interaction import Robot
from mock_robot_interaction import Mock_Robot
from sentiment_analysis import Classifier, sentiment

AUTO_SPLIT = True

def main():
    robot = Mock_Robot()
    classifier = Classifier()

    print("QT Robot will tell you a story. Which one do you want to hear?\n")
    textfiles = {}
    with os.scandir('stories/') as entries:
        i = 1
        for entry in entries:
            print(str(i) + " - " + entry.name)
            textfiles[i] = entry.name
            i += 1

    print("Your choice : ")
    choice = int(input())
    with open("stories/" + textfiles.get(choice)) as f:
        text = f.read()

    sentences_with_sentiment = classifier.classify(text, AUTO_SPLIT)

    for sentence in sentences_with_sentiment.keys():
        if sentiment(sentences_with_sentiment[sentence]) != sentiment.NEUTRAL:
            if sentiment(sentences_with_sentiment[sentence]) != last_sentiment:
                last_sentiment = sentiment(sentences_with_sentiment[sentence])
                print("SENTIMENT -> " + sentences_with_sentiment[sentence])
                robot.showEmotion(sentiment(sentences_with_sentiment[sentence]))
                robot.playGesture(sentiment(sentences_with_sentiment[sentence]))
                robot.say_serv(sentence)
            else:
                print("same as before -> speaking with lips")
                robot.say_serv_lips(sentence)
                last_sentiment = sentiment.NEUTRAL
        else:
            print("neutral -> speaking with lips")
            robot.say_serv_lips(sentence)
            last_sentiment = sentiment.NEUTRAL
        time.sleep(1)
        #rospy.sleep(0.1)
        print("\n") 


if __name__ == "__main__":
    main()
