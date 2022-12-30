#!/usr/bin/env python
import sys
import rospy
from qt_robot_interface.srv import *

if __name__ == '__main__':
    rospy.init_node('my_tutorial_node')
    rospy.loginfo("my_tutorial_node started!")

    # define a ros service
    speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
    
    # block/wait for ros service
    rospy.wait_for_service('/qt_robot/speech/say') 
   
    try:
        # call a ros service with text message
        speechSay("Hello! This is QT talking using text to speech")
    except KeyboardInterrupt:
        pass

    rospy.loginfo("finsihed!")

