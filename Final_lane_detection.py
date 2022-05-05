import os

import cv2
from cv_bridge import CvBridge

import numpy as np

import rospy
from sensor_msgs.msg import Image

from canny_func import region_of_interest, make_points, average, display_lines


class Lane_Detector:
    def __init__(self):
        self.pub = rospy.Publisher('/TeslaRoadster/camera_node/image/detected', Image, queue_size=10)

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
        return img_w_lanes

    def callback(self, msg):
        rospy.loginfo('Got image')
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
        processed_img = self.line_detection(cv_image)
        rospy.loginfo('Publishing image')
        self.pub.publish(bridge.cv2_to_imgmsg(processed_img, "bgr8"))

    def subscriber(self):
        rospy.Subscriber("/TeslaRoadster/camera_node/image/raw", Image, self.callback)


if __name__ == '__main__':

    rospy.init_node('Lane_detection')
    try:
        dt_objdt = Lane_Detector()
        dt_objdt.subscriber()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
