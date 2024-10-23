from pathlib import Path
import pandas as pd
import cv2
import numpy as np

# Class labels and their corresponding colors (converted to BGR format).
alphabet = ["dam", "groyne", "lock", "sluice", "weir"]
colors = {
    "dam": (77, 219, 235),
    "groyne": (140, 207, 158),
    "lock": (243, 243, 243),
    "sluice": (180, 179, 76),
    "weir": (82, 42, 203)
}

thickness = 12

label_root = Path(r"G:\ultralytics-main\dataset\temp\labels_yolo")
image_root = Path(r"G:\ultralytics-main\dataset\temp\images")
output_root = Path(r"G:\ultralytics-main\dataset\temp\output")

output_root.mkdir(parents=True, exist_ok=True)

def paint(label_file, image_file, output_file):
    df = pd.read_csv(label_file, sep=" ", names=['id', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'])
    df['id'] = df['id'].apply(lambda x: alphabet[int(x)])

    img = cv2.imread(str(image_root / image_file))
    h, w = img.shape[:2]

    df[['x1', 'x2', 'x3', 'x4']] = df[['x1', 'x2', 'x3', 'x4']].apply(lambda x: x * w)
    df[['y1', 'y2', 'y3', 'y4']] = df[['y1', 'y2', 'y3', 'y4']].apply(lambda y: y * h)

    for _, row in df.iterrows():
        color = colors[row['id']]
        points = np.array([[row['x1'], row['y1']], [row['x2'], row['y2']],
                           [row['x3'], row['y3']], [row['x4'], row['y4']]], np.int32)
        points = points.reshape((-1, 1, 2))
        img = cv2.polylines(img, [points], isClosed=True, color=color, thickness=thickness)

    cv2.imwrite(str(output_file), img)

for label_file in label_root.iterdir():
    image_file = label_file.name.replace(".txt", ".jpg")
    output_file = output_root / image_file
    paint(label_file, image_file, output_file)

print("complete")
