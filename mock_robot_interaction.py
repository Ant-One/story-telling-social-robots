
from sentiment_analysis import sentiment

class Mock_Robot:

    def __init__(self) -> None:
        print('story_node')
        print("story_node started!")

        """ self.speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
        self.gesture_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
        self.emotion_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=10)

        self.speech_serv = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        self.speech_serv_lips = rospy.ServiceProxy('/qt_robot/behavior/talkText', behavior_talk_text)
        rospy.sleep(3) """
        
    
    def showEmotion(self, emotion):
        if emotion == sentiment.ANGRY:
            self.emotion_pub.publish("QT/angry")
        elif emotion == sentiment.DISGUSTED:
            self.emotion_pub.publish("QT/disgusted")
        elif emotion == sentiment.AFRAID:
            self.emotion_pub.publish("QT/afraid")
        elif emotion == sentiment.JOYFUL:
            self.emotion_pub.publish("QT/happy")
        #elif emotion == sentiment.NEUTRAL:
            #emotion_pub.publish("QT/neutral")
        elif emotion == sentiment.SAD:
            self.emotion_pub.publish("QT/sad")
        elif emotion == sentiment.SURPRISED:
            self.emotion_pub.publish("QT/surprised")

        print("showed emotion: " + str(emotion))

    def playGesture(self, gesture):
        if gesture == sentiment.ANGRY:
            print("ANGRY GESTURE")
        elif gesture == sentiment.DISGUSTED:
            print("DISGUSTED GESTURE")
        elif gesture == sentiment.AFRAID:
            print("AFRAID GESTURE")
        elif gesture == sentiment.JOYFUL:
            print("HAPPY GESTURE")
        #elif gesture == sentiment.NEUTRAL:
            #gesture_pub.publish("QT/neutral")
        elif gesture == sentiment.SAD:
            print("SAD GESTURE")
        elif gesture == sentiment.SURPRISED:
            print("SURPRISE GESTURE")

        print("played gesture " + str(gesture))

    def say(self, text):
        #self.speech_pub.publish(text)
        print("Said: " + text)

    def say_serv(self, text):
        print("Speech service saying: " + text)
        #rospy.wait_for_service('/qt_robot/speech/say') 
        #print(text)

    def say_serv_lips(self, text):
        print("Speech service saying with lip-sync: " + text)
        #rospy.wait_for_service('/qt_robot/behavior/talkText')
        #print(text)