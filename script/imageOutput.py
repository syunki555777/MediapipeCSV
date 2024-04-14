import cv2
import os
import pandas as pd
import concurrent.futures


# Worker function to process each image
def worker(image_path):
    img = cv2.imread(image_path)

    # Use mediapipe for face meshing and blend shapes
    # face_meshes, blend_shapes = Your mediapipe processing function

    # For this example, assume the shape of the image as the face mesh and blend shape
    face_meshes = blend_shapes = img.shape

    return {'path': image_path, 'face_meshes': face_meshes, 'blend_shapes': blend_shapes}


# Main function to multi-thread process images
def process_images_and_output_to_csv(directory, csv_output):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_files = [os.path.join(directory, file)
                       for file in os.listdir(directory)
                       if file.endswith((".png", ".jpg", ".jpeg"))]
        result = list(executor.map(worker, image_files))

    df = pd.DataFrame(result)
    df.to_csv(csv_output)


# usage
process_images_and_output_to_csv('path_to_images', 'output.csv')
