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


def img_pred(img, folder_name, img_name):
    # Load a model
    total_count = 0
    model = YOLO('/home/cyber-makarov/pallet_fast/model/pallets_best.pt')  # pretrained YOLOv8n model
    results = model(img)[0]  # return a generator of Results objects
    detections = sv.Detections.from_ultralytics(results)
    #detect_rest = results.show()
    count = len(results.boxes)
    total_count += count
    full_path = create_folder_if_not_exists(folder_name)
    img_path = os.path.join(full_path, f"{img_name}.jpg")

    if img.mode == 'RGBA':
        img = img.convert('RGB')

        # Save the input image with a different variable name
    img.save(img_path)

    return total_count, img_path