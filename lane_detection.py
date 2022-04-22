import os

import cv2
from cv_bridge import CvBridge

import numpy

import rospy
from sensor_msgs.msg import Image

class GetImage(object):
    def __init__(self):
        # Update frequency 
        self.freq = rospy.Rate(1)
        self.bridge = CvBridge()

        # Publisher
        self.pub = rospy.Publisher('imagetimer', Image, queue_size=10)

    def line_detection(self, image):
        # line detection code
        self.pub.publish(self.bridge.cv2_to_imgmsg(image)) 

    def callback(self, msg):
        rospy.loginfo('Got image')
        image = self.bridge.imgmsg_to_cv2(msg)
        self.line_detection(image)

    def start(self):
        rospy.loginfo('Reading images...')
        while not rospy.is_shutdown():
            rospy.logifo('Publishing image')
            if self.image is not None:
                rospy.Subscriber("/tesla_roadster/camera_node/image/raw", Image, self.callback)
            self.freq.sleep()

if __name__ == '__main__':
    rospy.init_node("imagetimer111", anonymous=True)
    getImageNode = GetImage()
    getImageNode.start()




