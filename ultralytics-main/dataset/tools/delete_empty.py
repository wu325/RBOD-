# 删除没有标签文件的图片
import os
from pathlib import Path

def remove_images_without_labels(im_dir, lb_dir):
    """
    Remove images that do not contain target instances.
    Args:
        im_dir (str): Image directory
        lb_dir (str): label directory
    """
    im_dir = Path(im_dir)
    lb_dir = Path(lb_dir)

    for im_file in im_dir.glob("*.jpg"):
        label_file = lb_dir / (im_file.stem + ".txt")
        if not label_file.exists():
            print(f"Deleting {im_file} because it has no label.")
            os.remove(im_file)

print("删除--train--中的无标签图片")
remove_images_without_labels("/root/autodl-tmp/ultralytics-main/dataset/YRBD_ms/images/train",
                             "/root/autodl-tmp/ultralytics-main/dataset/YRBD_ms/labels/train")
print("删除--val--中的无标签图片")
remove_images_without_labels("/root/autodl-tmp/ultralytics-main/dataset/YRBD_ms/images/val",
                             "/root/autodl-tmp/ultralytics-main/dataset/YRBD_ms/labels/val")
print("删除--test--中的无标签图片")
remove_images_without_labels("/root/autodl-tmp/ultralytics-main/dataset/YRBD_ms/images/test",
                             "/root/autodl-tmp/ultralytics-main/dataset/YRBD_ms/labels/test")