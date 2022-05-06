# <div align=center>duckietown_yolov5</div>
#### <div align="center">" This repository is created for object recognition functionality of Duckiebot, </div>
#### <div align="center"> which reads the camera view of a duckiebot and detects the obstacle in the front. "</div>

***
# I. Introduction to ROS

### A. How to install ROS Noetic
1. You can take a look at the ROS Wiki page to follow <a href="http://wiki.ros.org/noetic/Installation/Ubuntu">instructions to ROS Noetic installation</a>.

### B. How to create ROS Workspace and Package
1. Create a ROS workspace

       $ mkdir -p ~/catkin_ws/src
       $ cd ~/catkin_ws/
       $ catkin_make
       $ source devel/setup.bash

2. Get into your ROS workspace

       $ cd ~/catkin_ws/src
       
3. Copy a ROS Package

       $ git clone https://github.com/ldw200012/duckietown_yolov5.git

4. Run below commands to configure your ROS Package

       $ cd ~/catkin_ws
       $ catkin_make
       $ source devel/setup.bash (This command must be run on every shell you are using for ROS from now on)
       
# II. Introduction to YOLOv5

### A. Custom the program (you can skip to B if you only want to detect duckie)

1. Prepare a dataset 

      i. Data preparation from duckiebot camera (You can skip this step if you already have your own images).
       
       $ rosrun image_transport republish compressed in:=/[duckiebot_name]/camera_node/image raw out:=/[duckiebot_name]/camera_node/image/raw
       $ cd [folder_directory_to_save_images]
       $ rosrun image_view image_saver image:=/[duckiebot_name]/camera_node/image/raw _save_all_image:=false _filename_format:=foo.jpg __name:=image_saver
       
      Now you can save image to the directory whenever you call the below command
       
       $ rosservice call /image_saver/save      
     
      ii. Data Annotation

      - Follow the instructions in Roboflow https://blog.roboflow.com/vott/
      
      iii. Dataset Creation
       
      - Follow the instructions in Roboflow https://www.youtube.com/watch?v=MdF6x6ZmLAY until 15:40.
      
        From now on, you need to remember the "<b>link</b>" provided by Roboflow. (Choose 'Terminal' among 'Jupyter/Terminal/Raw URL')
        <br>
        <br>
        
2. Train the dataset:

      i. Clean some file directories

       $ roscd duckietown_yolov5/content/
       $ rm -rf *
       
       $ roscd duckietown_yolov5/scripts/       
       delete all the files except 'detect.py' and 'detect_and_publish.py'
      <br>
      
      ii. Clone a git repository below

       $ roscd duckietown_yolov5/content/
       $ git clone https://github.com/ultralytics/yolov5
       $ roscd duckietown_yolov5/content/yolov5/
       $ git reset --hard 886f1c03d839575afecb059accf74296fad395b6
      <br>
       
      iii. Install all requirements (ignore errors)

       $ pip install -qr requirements.txt
      <br>

      iv. Open Python and run below codes

       $ python
       >> import torch
       >> from IPython.display import Image, clear_output
       >> from utils.google_utils import gdrive_download
       >> 
       >> print('Setup complete. Using torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))
      <br>
      
      v. In '/content' folder, copy and paste the Terminal link from your Roboflow dataset.
       
      (If you see a question "replace data.yaml? [y]es, [n]o, [A]ll, [r]ename:", enter A for all)
       
       $ roscd duckietown_yolov5/content/
       $ curl -L "https://..." > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
       $ cat data.yaml      
      <br>
       
      vi. Open Python and run below codes

       $ python
       >> # define number of classes based on YAML
       >> import yaml
       >> with open("data.yaml", 'r') as stream:
       ..     num_classes = str(yaml.safe_load(stream)['nc'])
      <br>
       
      vii. Create your own .yaml file

       $ roscd duckietown_yolov5/content/yolov5/models/
       $ touch custom_yolov5s.yaml
       $ nano custom_yolov5s.yaml
       
      Then, paste the below cell into custom_yolov5s.yaml, save.
       
       # parameters
       nc: {num_classes}  # number of classes
       depth_multiple: 0.33  # model depth multiple
       width_multiple: 0.50  # layer channel multiple
       
       # anchors
       anchors:
         - [10,13, 16,30, 33,23]  # P3/8
         - [30,61, 62,45, 59,119]  # P4/16
         - [116,90, 156,198, 373,326]  # P5/32

       # YOLOv5 backbone
       backbone:
         # [from, number, module, args]
         [[-1, 1, Focus, [64, 3]],  # 0-P1/2
          [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
          [-1, 3, BottleneckCSP, [128]],
          [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
          [-1, 9, BottleneckCSP, [256]],
          [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
          [-1, 9, BottleneckCSP, [512]],
          [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
          [-1, 1, SPP, [1024, [5, 9, 13]]],
          [-1, 3, BottleneckCSP, [1024, False]],  # 9
         ]

       # YOLOv5 head
       head:
         [[-1, 1, Conv, [512, 1, 1]],
          [-1, 1, nn.Upsample, [None, 2, 'nearest']],
          [[-1, 6], 1, Concat, [1]],  # cat backbone P4
          [-1, 3, BottleneckCSP, [512, False]],  # 13

          [-1, 1, Conv, [256, 1, 1]],
          [-1, 1, nn.Upsample, [None, 2, 'nearest']],
          [[-1, 4], 1, Concat, [1]],  # cat backbone P3
          [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)

          [-1, 1, Conv, [256, 3, 2]],
          [[-1, 14], 1, Concat, [1]],  # cat head P4
          [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)

          [-1, 1, Conv, [512, 3, 2]],
          [[-1, 10], 1, Concat, [1]],  # cat head P5
          [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)

          [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
         ]
      <br>

      viii. Train your own dataset in the '/yolov5' directory.

       $ roscd duckietown_yolov5/content/yolov5/
       $ python train.py --img 416 --batch 16 --epochs 100 --data '../data.yaml' --cfg ./models/custom_yolov5s.yaml --weights '' --name yolov5s_results  --cache
       
      You can change the epochs number as you want
      <br>
      <br>

      ix. Check for trained weights

       $ ls runs/
       $ ls runs/train/yolov5s_results/weights
       
      You will see two * .pt files, which are your weights files.
      <br>
      <br>
      
      x. THE MOST IMPORTANT STEP
      * <b>Move all the files and subfolders from 'duckietown_yolov5/content/yolov5/' to 'duckietown_yolov5/scripts/' except 'detect.py'.</b>

### B. How to run the program
1. Object Detection
        
      - In shell 1:
     
       $ rosrun image_transport republish compressed in:=/[duckiebot_name]/camera_node/image raw out:=/[duckiebot_name]/camera_node/image/raw
       
      - In shell 2:
     
       $ roscd duckietown_yolov5/script/
       $ python detect_and_publish.py
       
      - In shell 3:
       
       $ dts start_gui_tools [duckiebotname]
       # rqt_image_view

# III. Dataset

- The Dataset has been provided by https://github.com/duckietown/duckietown-objdet

***
# About the Project

#### Module Name: CO-548-A RIS Project
#### Instructor: Prof. Francesco Maurelli
#### Contributors: Dongwook Lee, Joudi Alzaeem, Kamilla Shagazatova


