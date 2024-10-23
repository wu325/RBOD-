# RBOD: An annotated satellite imagery dataset for automated river barrier object detection  
The RBOD is the first publicly available dataset for river barrier object detection. It comprises 4,872 high-resolution satellite images and 11,741 meticulously annotated oriented bounding boxes (OBBs), encompassing five classes of river barriers. Five mainstream oriented object detection algorithms, including YOLOv8-OBB, Oriented R-CNN, Rotated Faster R-CNN, R3Det, and Rotated RetinaNet, were chosen for performance evaluation on the RBOD dataset, providing a benchmark for comparing the detection performance of various state-of-the-art algorithms.  In this repository, We provide the necessary code for generating, statistical analysis, and validating the dataset.

## Files description:  
· dataset_process - The folder containing the dataset generation code  

· dataset_statistics - The code for performing statistical analysis of the dataset's features  

· mmrotate-0.3.4 - The mmrotate framework for training and validation Oriented R-CNN, Rotated Faster R-CNN, R3Det, and Rotated RetinaNet models.  

· ultralytics-main - The scripts for training and validation YOLOV8-OBB model.  

· modles - The configuration files and training weights for the above model provide the performance benchmark for this dataset.  

## Dataset download:  
The RBOD dataset can be downloaded from:  

## training models:  
All experiments in this study were conducted in an environment with Python 3.9.19 and torch 2.2.2+cu121.  

· For training and testing of various models (including Oriented R-CNN, Rotated Faster R-CNN, R3Det, and Rotated RetinaNet ) under the mmrotate framework, please refer to https://github.com/open-mmlab/mmrotate?tab=readme-ov-file.  

· For training and testing of YOLOV8-OBB, please refer to https://github.com/ultralytics/ultralytics.  
