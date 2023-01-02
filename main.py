import os
import time

#import rospy

#from robot_interaction import Robot
from mock_robot_interaction import Mock_Robot
from sentiment_analysis import Classifier, sentiment
import story_gen

AUTO_SPLIT = True

def main():

    print("""


    _________________                                                                                             
   / ____/ ___/_  __/                                                                                             
  / __/  \__ \ / /                                                                                                
 / /___ ___/ // /                                                                                                 
/_____//____//_/_______          __                   _         _____ __                  ______     ____         
              / ____/ /__  _____/ /__________  ____  (_)____   / ___// /_____  _______  _/_  __/__  / / /__  _____
             / __/ / / _ \/ ___/ __/ ___/ __ \/ __ \/ / ___/   \__ \/ __/ __ \/ ___/ / / // / / _ \/ / / _ \/ ___/
            / /___/ /  __/ /__/ /_/ /  / /_/ / / / / / /__    ___/ / /_/ /_/ / /  / /_/ // / /  __/ / /  __/ /    
           /_____/_/\___/\___/\__/_/   \____/_/ /_/_/\___/   /____/\__/\____/_/   \__, //_/  \___/_/_/\___/_/     
                                                                                 /____/                           

""")

    robot = Mock_Robot()
    classifier = Classifier()

    print("QT Robot will tell you a story. Which one do you want to hear?\n \
    \t -- Select the last option to generate new ones or put text files in stories/\n")
    textfiles = {}
    with os.scandir('stories/') as entries:
        i = 1
        for entry in entries:
            print(str(i) + " - " + entry.name)
            textfiles[i] = entry.name
            i += 1
        print("\n" + str(i) + " - Generate new story\n")

    print("Your choice : ")
    choice = int(input())
    if (choice == i):
        story_gen.main()
        main()
    else:
        with open("stories/" + textfiles.get(choice)) as f:
            text = f.read()

    sentences_with_sentiment = classifier.classify(text, AUTO_SPLIT)

    last_sentiment = ()

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
        #time.sleep(1)
        #rospy.sleep(0.1)
        print("\n") 


if __name__ == "__main__":
    main()
