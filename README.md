# Code for the RIS Project course at Jacobs University Bremen  

This is an object avoidance project using computer vision with [Duckiebots](https://www.duckietown.org/)  
  
Team Members: Bogdan Belenis, Keagan Holmes, Eunchong Kim  
  
  
## To run this code:  

Add the following to the "~/.bashrc" file:  
```
export "ROS_MASTER_URI=http://TeslaRoadster.local:11311"  
```

In shell 1:  
```
rosrun image_transport republish compressed in:=/TeslaRoadster/camera_node/image raw out:=/TeslaRoadster/camera_node/image/raw
```

In shell 2:
```
cd ./object_detection/scripts
python3 lane_object_detection.py
```

In shell 3:
```
dts start_gui_tools TeslaRoadster
rqt_image_view

```
## Install Requirements:
```
cd ./object_detection/scripts
pip install -r requirements.txt
```
