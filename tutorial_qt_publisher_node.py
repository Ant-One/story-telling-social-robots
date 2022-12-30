#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import String

if __name__ == '__main__':
    rospy.init_node('my_tutorial_node')
    rospy.loginfo("my_tutorial_node started!")

   # creating a ros publisher
    speechSay_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
    gesturePlay_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
    emotionShow_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=10)
    rospy.sleep(3.0)

   # publish a text message to TTS
    #speechSay_pub.publish("Hello! my name is QT!")
    
    # creating a ros publisher
   
    emotionShow_pub.publish("QT/happy")
    
    # creating a ros publisher

    gesturePlay_pub.publish("QT/clapping")

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

    rospy.loginfo("finsihed!")

