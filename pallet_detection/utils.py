import os

from ultralytics import YOLO
import supervision as sv
from PIL import Image
from io import BytesIO
import cv2

def create_folder_if_not_exists(folder_name):
    """
    Create a folder if it doesn't exist.

    Args:
        folder_name (str): The name of the folder to create.

    Returns:
        str: The path of the folder.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder created: {folder_name}")
    else:
        print(f"Folder already exists: {folder_name}")

    return folder_name

#
def image_prediction(img, folder_name, img_name):
    total_count = 0
    model = YOLO('/home/imsadka/Documents/GoodFolks/pallets_app/model/pallets_best.pt')
    results = model(img)[0]
    detections = sv.Detections.from_ultralytics(results)
    count = len(results.boxes)
    total_count += count
    full_path = create_folder_if_not_exists(folder_name)
    img_path = os.path.join(full_path, f"{img_name}")

    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(img_path)

    return total_count, img_path