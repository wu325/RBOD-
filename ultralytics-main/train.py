import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

# 训练参数官方详解链接：https://docs.ultralytics.com/modes/train/#resuming-interrupted-trainings:~:text=a%20training%20run.-,Train%20Settings,-The%20training%20settings

if __name__ == '__main__':
    model = YOLO('cfg/yolov8n-obb.yaml')
    # model.load('yolov8n.pt') # loading pretrain weights
    model.train(data='dataset/YRBD_ms/data.yaml',
                cache=False,
                imgsz=1024,
                epochs=100,
                batch=16,
                close_mosaic=10,
                workers=4,
                device=0,
                optimizer='SGD',
                lr0=0.01,
                lrf=0.01,
                project='runs/train',
                name='yolov8n-obb',
                )