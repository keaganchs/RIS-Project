#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image

import os
import argparse
import torch
import cv2
from detect import detect
from distance_detection import find_marker, distance_to_camera
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from cv_bridge import CvBridge, CvBridgeError


# def callback(data, opt):
#     pub = rospy.Publisher('/JoudiDuck/camera_node/image/detected', Image, queue_size=10)
    
#     # Save rostopic images into directory
#     bridge = CvBridge()
#     cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    
#     img_save_path = "../content/test/frame_images/frame.jpg"
#     if os.path.exists(img_save_path):
#         os.remove(img_save_path)
#         print("Ready for new frame")
#     cv2.imwrite(img_save_path, cv_image)

#     with torch.no_grad():
#         if opt.update:  # update all models (to fix SourceChangeWarning)
#             for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
#                 im0 = detect(opt)
#                 strip_optimizer(opt.weights)
#         else:
#             im0 = detect(opt)

#     # Publish into new rostopic
# #     img_read_path = output_dir + "/frame.jpg"
# #     cv_image_detected = cv2.imread(img_read_path)
#     pub.publish(bridge.cv2_to_imgmsg(im0, "bgr8"))

#     # Delete image and folder
# #     os.remove(img_read_path)
# #     os.rmdir(output_dir)


# def my_subscriber(opt):
#     rospy.Subscriber("/JoudiDuck/camera_node/image/raw", Image, callback, opt)
  



class Object_Detector:
    def __init__(self, opt):
        self.opt = opt
        self.pub = rospy.Publisher('/JoudiDuck/camera_node/image/detected', Image, queue_size=10)
        
    def callback(self, data):
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    
        img_save_path = "../content/test/frame_images/frame.jpg"
        if os.path.exists(img_save_path):
            os.remove(img_save_path)
            print("Ready for new frame")
        cv2.imwrite(img_save_path, cv_image)

        with torch.no_grad():
            if opt.update:  # update all models (to fix SourceChangeWarning)
                for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                    im0 = detect(opt)
                    strip_optimizer(opt.weights)
            else:
                im0 = detect(opt)

        self.pub.publish(bridge.cv2_to_imgmsg(im0, "bgr8"))
        
    def subscriber(self):
        rospy.Subscriber("/JoudiDuck/camera_node/image/raw", Image, self.callback)

if __name__ == '__main__':
    
    rospy.init_node('duckietown_yolov5')   
    try:
        # Detection from directory and save
        parser = argparse.ArgumentParser()
        parser.add_argument('--weights', nargs='+', type=str, default='runs/train/yolov5s_results/weights/best.pt', help='model.pt path(s)')
        parser.add_argument('--source', type=str, default='../content/test/frame_images', help='source')  # file/folder, 0 for webcam
        parser.add_argument('--img-size', type=int, default=416, help='inference size (pixels)')
        parser.add_argument('--conf-thres', type=float, default=0.4, help='object confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
        parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser.add_argument('--view-img', action='store_true', help='display results')
        parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
        parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
        parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
        parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
        parser.add_argument('--augment', action='store_true', help='augmented inference')
        parser.add_argument('--update', action='store_true', help='update all models')
        parser.add_argument('--project', default='runs/detect', help='save results to project/name')
        parser.add_argument('--name', default='exp', help='save results to project/name')
        parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        opt = parser.parse_args()
        print(opt)
        check_requirements()
        
        dt_objdt = Object_Detector(opt)
        dt_objdt.subscriber()
        
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

        
        
        
