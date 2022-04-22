import os

import cv2
from cv_bridge import CvBridge

import numpy

import rospy
from sensor_msgs.msg import Image

cv2.imread()

class Robot(object):
    def __init__(self):
        # Update frequency 
        self.freq   = rospy.Rate(1)
        self.image  = None
        self.bridge = CvBridge()

        # Publisher
        self.pub = rospy.Publisher('imagetimer', Image, queue_size=10)

        # Subscriber
        rospy.Subscriber("/tesla_roadster/camera_node/image/raw", Image, self.callback)

    def callback(self, msg):





