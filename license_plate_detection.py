from multiprocessing import freeze_support

import cv2
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
import os
from ultralytics import YOLO


def xml_to_yolo(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]

def convert_dataset():
    for filename in os.listdir("annotations"):

        tree = ET.parse(f"annotations/{filename}")
        root = tree.getroot()
        name = root.find("filename").text.replace(".png", "")
        width = int(root.find("size").find("width").text)
        height = int(root.find("size").find("height").text)

        for obj in root.findall('object'):
            box = []
            for x in obj.find("bndbox"):
                box.append(int(x.text))

            yolo_box = xml_to_yolo(box, width, height)
            line = f"0 {yolo_box[0]} {yolo_box[1]} {yolo_box[2]} {yolo_box[3]}"

            with open(f"train/labels/{name}.txt", "a") as file:
                # Write a line to the file
                file.write(f"{line}\n")

#convert_dataset()


if __name__ == '__main__':
                freeze_support()
model = YOLO('yolov8n.yaml')
result = model.train(data="config.yaml",device="0",epochs=1,verbose=True,plots=True,save=True)
#result = model.predict(source="train/images/cars2.png",save=True)
