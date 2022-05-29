import os

import cv2
from cv_bridge import CvBridge

import numpy as np

import rospy
from sensor_msgs.msg import Image

# Lane Detection
from canny_func import region_of_interest, make_points, average, display_lines

# Object Detectiob
import argparse
import torch
from detect import detect
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path


class Detector:
    def __init__(self, opt):
        self.opt = opt
        self.pub = rospy.Publisher('/TeslaRoadster/camera_node/image/detected', Image, queue_size=10)

    def line_detection(self, image):
        # =========== line detection code ===========
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

        # Calling line detection function ================
        processed_img = self.line_detection(cv_image)
        # ====================================

        # Object detection ====================
        img_save_path = "../content/test/frame_images/frame.jpg"
        if os.path.exists(img_save_path):
            os.remove(img_save_path)
            print("Ready for new frame")
        cv2.imwrite(img_save_path, processed_img)

        with torch.no_grad():
            # update all models (to fix SourceChangeWarning)
            if opt.update:
                for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                    final_img = detect(opt)
                    strip_optimizer(opt.weights)
            else:
                final_img = detect(opt)
        # ====================================

        # Publishing
        rospy.loginfo('Publishing image')
        self.pub.publish(bridge.cv2_to_imgmsg(final_img, "bgr8"))

    def subscriber(self):
        rospy.Subscriber("/TeslaRoadster/camera_node/image/raw", Image, self.callback)


if __name__ == '__main__':

    rospy.init_node('detection')
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--weights', nargs='+', type=str, default='runs/train/yolov5s_results/weights/best.pt', help='model.pt path(s)')
        parser.add_argument('--source', type=str, default="../content/test/frame_images/", help='source')
        parser.add_argument('--img-size', type=int, default=416, help='inference size (pixels)')
        parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
        parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser.add_argument( '--view-img', action='store_true', help='display results')
        parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
        parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
        parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
        parser.add_argument( '--agnostic-nms', action='store_true', help='class-agnostic NMS')
        parser.add_argument('--augment', action='store_true', help='augmented inference')
        parser.add_argument('--update', action='store_true', help='update all models')
        parser.add_argument('--project', default='runs/detect', help='save results to project/name')
        parser.add_argument('--name', default='exp', help='save results to project/name')
        parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        opt = parser.parse_args()
        check_requirements()

        dt_objdt = Detector(opt)
        dt_objdt.subscriber()

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
