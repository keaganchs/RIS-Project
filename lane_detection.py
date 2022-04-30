import os

import cv2
from cv_bridge import CvBridge

import numpy as np

import rospy
from sensor_msgs.msg import Image

from canny_func import region_of_interest, make_points, average, display_lines


class GetImage(object):
    def __init__(self):
        # Update frequency
        self.freq = rospy.Rate(1)
        self.bridge = CvBridge()

        # Publisher
        self.pub = rospy.Publisher('imagetimer', Image, queue_size=10)

    def line_detection(self, image):
        # =========== line detection code ===========
        # img = cv2.imread("lane detection images/test4.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 100, 200)
        roi = region_of_interest(edges)
        lines = cv2.HoughLinesP(roi, 2, np.pi/180, 100,
                                np.array([]), minLineLength=40, maxLineGap=5)
        copy = np.copy(image)
        averaged_lines = average(copy, lines)
        black_lines = display_lines(copy, averaged_lines)
        img_w_lanes = cv2.addWeighted(copy, 0.8, black_lines, 1, 1)
        # =============================================
        self.pub.publish(self.bridge.cv2_to_imgmsg(img_w_lanes, "bgr8"))

    def callback(self, msg):
        rospy.loginfo('Got image')
        image = self.bridge.imgmsg_to_cv2(msg)
        self.line_detection(image)

    def start(self):
        rospy.loginfo('Reading images...')
        while not rospy.is_shutdown():
            rospy.loginfo('Publishing image')
            # if self.image is not None:
            rospy.Subscriber(
                "/hippiehippo/camera_node/image/raw", Image, self.callback)
            self.freq.sleep()


if __name__ == '__main__':
    rospy.init_node("imagetimer111", anonymous=True)
    getImageNode = GetImage()
    getImageNode.start()
