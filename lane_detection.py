import os

import cv2
from cv_bridge import CvBridge

import numpy

import rospy
from sensor_msgs.msg import Image

cv2.imread()

class GetImage(object):
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
        rospy.loginfo('Got image')
        self.image = self.bridge.imgmsg_to_cv2(msg)

    def start(self):
        rospy.loginfo('Reading images...')
        while not rospy.is_shutdown():
            rospy.logifo('Publishing image')
            if self.image is not None:
                self.pub.publish(self.bridge.cv2_to_imgmsg(self.image))
            self.freq.sleep()

if __name__ == '__main__':
    rospy.init_node("imagetimer111", anonymous=True)
    getImageNode = GetImage()
    getImageNode.start()





