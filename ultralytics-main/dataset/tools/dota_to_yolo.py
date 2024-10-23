# Convert DOTA format TXT label files to YOLO format TXT label files.
from ultralytics.data.converter import convert_dota_to_yolo_obb

convert_dota_to_yolo_obb(r'/dataset/YRBD')
