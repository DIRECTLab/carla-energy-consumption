import cv2
import os
import sys

import torch
from torch import optim
import torch.nn as nn

import numpy as np
from torch.utils.data import DataLoader

import cv2
import matplotlib.pyplot as plt

import yaml
import math
from tqdm import tqdm

import pandas as pd
import copy
from ultralytics import YOLO


def get_edges(img):
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_grey, (3, 3), 0)
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=300) # Canny Edge Detection

    # cv2.imshow('Sobel of edges', edges)
    # cv2.waitKey(0)
    
    # cv2.destroyAllWindows()

    img_blur = cv2.blur(edges, (3, 3), 0)
    
    sobel_x = cv2.Sobel(src=img_blur, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3) # Sobel Edge Detection on the X axis
    img_blur = cv2.blur(sobel_x, (3, 3), 0)

    _, thresh4 = cv2.threshold(img_blur, 127, 255, cv2.THRESH_BINARY)

    return thresh4

def get_tire_position(result, i):
    x1, y1, x2, y2 = results[0].boxes[i].xyxy.numpy().astype(int)[0]

    # cv2.rectangle(test_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    left_wheel = (x1, y2)
    right_wheel = (x2, y2)
    
    return left_wheel, right_wheel

def find_line(img):
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_grey, 245, 255, cv2.THRESH_BINARY)
    y_cropping = thresh.shape[0] // 4
    cropped_thresh = thresh[y_cropping:thresh.shape[0], :]

    contours, _ = cv2.findContours(cropped_thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if True:
            cv2.drawContours(cropped_thresh,[cnt],0,(0,255,0),2)

    one_third_way = len(cropped_thresh[0]) // 3
    two_third_way = 2 * one_third_way
    start_y = len(cropped_thresh) - 1
    center_of_white_line = 0
    left_of_line = (0, 0)
    right_of_line = (0, 0)


    for i in range(0, start_y, 1):
        for j in range(0, two_third_way, 1):
            if cropped_thresh[i, j] == 255 and cropped_thresh[i - 1, j] == 255:
                left_of_line = (j, i + y_cropping)

                while cropped_thresh[i, j] == 255 or cropped_thresh[i, j + 1] == 255:
                    j += 1
                right_of_line = (j, i + y_cropping)

                break

    middle_x = (right_of_line[0] + left_of_line[0]) // 2
    center_of_white_line = (middle_x, left_of_line[1])

    return left_of_line, right_of_line, center_of_white_line

def get_closet_car(centers_in_pixels, center_of_white_line, car_info):
    least_distance = np.inf
    closest_car = (0, 0)
    closest_index = -1

    for i, center in enumerate(centers_in_pixels):
        if center[0] - center_of_white_line[0] > 0:
            # Compute L2 distance between mids
            distance = math.sqrt((center[1] - center_of_white_line[1]) ** 2 + (center[0] - center_of_white_line[0]) ** 2)
            slope = (center[1] - center_of_white_line[1]) / (center[0] - center_of_white_line[0])
            if distance < least_distance and car_info[i][-2] > 350 and distance < 900 and abs(slope) < 0.8:
                least_distance = distance
                closest_car = car_info[i][2]
                closest_index = i



    return least_distance, closest_car, closest_index





if __name__ == "__main__":
    with open("yolo.yaml", "r") as f:
        classes = yaml.safe_load(f)
    print(classes)

    folders = os.listdir("data/frames")[1:4]
    for folder_num, folder in enumerate(folders):
        yolo = YOLO("yolov8x-seg.pt")

    # folder = "DWARF_20230928141733807"
        images = [f"data/frames/{folder}/" + i for i in os.listdir(f"data/frames/{folder}")]
        # images = images[:400]
        df_csv = pd.DataFrame(columns = ["image_name", "anchor_point_x", "anchor_point_y", "car_center_x", "car_center_y", "left_tire_x", "left_tire_y", "right_tire_x", "right_tire_y", "frame_id", "vehicle_id"])
        dataloader = DataLoader(images, batch_size=1)

        loop = tqdm(dataloader)
        good_anchor_point = (0, 0)
        good_anchor_point_times_seen = 10
        anchor_point_threshold = 50.0
        
        for index, i in enumerate(loop):
            data = []
            labels = []
            results = yolo.track(i, persist=True, verbose=False)
            # Left, right, middle, height
            car_info = []
            x_y_info = []
            for result in results:
                if result == None or result.boxes == None or result.boxes.id == None or result.boxes.cls == None:
                    break
                centers_in_pixels = []
                cv_image = cv2.imread(result.path)
                black_box_image = copy.deepcopy(cv_image) 
                
                class_predictions = result.boxes.cls.cpu().numpy()
                tracking_ids = result.boxes.id.cpu().numpy()

                for j, class_label in enumerate(class_predictions):
                    label = result.names[int(class_label)]

                    if label == "car" or label == "truck" or label == "bus":
                        box = result.boxes.xyxy.cpu().numpy()[j]
                        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3]) - 10

                        
                        # Crop the images
                        cropped_image = cv_image[y:h, x:w]

                        # We need to mask all colors but white (excluding areas found by yolo, since those will be actual cars)
                        # This means that I will need to take a copy of the images, and replace all areas found by yolo with black boxes
                        black_box = np.zeros(cropped_image.shape)
                        black_box_image[y:h, x:w] = black_box


                        # ==================================================================================
                        # Get Tire positions
                        # ==================================================================================
                        (left_tire, right_tire) = get_tire_position(result, j)

                        middle_x = (right_tire[0] + left_tire[0]) // 2

                        # cv2.rectangle(cropped_image, (middle_x, (left_tire[1] + right_tire[1]) // 2), (middle_x, 0), (255, 0, 0), 2)
                        # cv2.putText(cropped_image, f"@{middle_x + x} pixels", (middle_x + 5, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 3)
                        # centers_in_pixels.append((middle_x, (left_tire[1] + right_tire[1]) // 2))
                        # car_info.append((left_tire, right_tire, (middle_x,  ((left_tire[1] + right_tire[1]) // 2)), h-y))
                        # centers_in_pixels.append((middle_x + x, ((left_tire[1] + right_tire[1]) // 2) + y))

                        # car_info.append((left_tire, right_tire, (middle_x, ((left_tire[1] + right_tire[1]) // 2)), h-y, tracking_ids[j]))
                        
                        centers_in_pixels.append((middle_x, (left_tire[1] + right_tire[1]) // 2))
                        car_info.append((left_tire, right_tire, (middle_x,  ((left_tire[1] + right_tire[1]) // 2)), h-y, tracking_ids[j]))
                        x_y_info.append((x, y))

                # ==================================================================================
                # Detect distance to white line
                # ==================================================================================
                left_of_line, right_of_line, center_of_white_line = find_line(black_box_image)

                if good_anchor_point == (0, 0):
                    good_anchor_point = ((left_of_line[0] + right_of_line[0]) // 2, (left_of_line[1] + right_of_line[1]) // 2)
                else:
                    if (left_of_line[0] + right_of_line[0]) // 2 + anchor_point_threshold > good_anchor_point[0] and (left_of_line[0] + right_of_line[0]) // 2 - anchor_point_threshold < good_anchor_point[1] and ((left_of_line[1] + right_of_line[1]) // 2) + anchor_point_threshold > good_anchor_point[1] and ((left_of_line[1] + right_of_line[1]) // 2) - anchor_point_threshold < good_anchor_point[1]:
                        good_anchor_point_times_seen += 1
                    else:
                        good_anchor_point_times_seen -= 1

                        if good_anchor_point_times_seen < 0:
                            good_anchor_point = ((left_of_line[0] + right_of_line[0]) // 2, (left_of_line[1] + right_of_line[1]) // 2)
                


                # cv2.rectangle(cv_image, (left_of_line[0], left_of_line[1]), (right_of_line[0], right_of_line[1]), (0, 255, 0), 10)


                # Plot the approximate center
                # cv2.rectangle(cv_image, (middle_x, (left_of_line[1] + right_of_line[1]) // 2), (middle_x, 0), (0, 0, 255), 2)
                # cv2.putText(cv_image, f"@{middle_x} pixels", (middle_x + 5, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                
                # ==================================================================================
                # Get Closest Car
                # ==================================================================================

                least_distance, closest_car, closest_index = get_closet_car(centers_in_pixels, center_of_white_line, car_info)

                if least_distance < np.inf:
                    closest_car_info = car_info[closest_index]
                    # Left, right, middle
                    # ["anchor_point_x", "anchor_point_y", "car_center_x", "car_center_y", "left_tire_x", "left_tire_y", "right_tire_x", "right_tire_y"]
                    split_image = i[0].split("/")
                    image_name = split_image[-2] + "/" + split_image[-1]
                    x = x_y_info[closest_index][0]
                    y = x_y_info[closest_index][1]
                    # Append info to df
                    df_csv.loc[len(df_csv.index)] = [image_name, good_anchor_point[0], good_anchor_point[1], closest_car_info[2][0] + x, closest_car_info[2][1] + y, closest_car_info[0][0] + x, closest_car_info[0][1] + y, closest_car_info[1][0] + x, closest_car_info[1][1] + y, image_name.split("/")[-1].split(".")[0], closest_car_info[-1]]
        
        df_csv.to_csv(f"data_{folder}.csv")
                    # Now create the distance in pixels as rect on image
                    # cv2.line(cv_image, (center_of_white_line), (closest_car), (255, 0, 255), 2)
                    # cv2.putText(cv_image, f"{round(least_distance, 2)} pixels", (center_of_white_line[0] + 5, center_of_white_line[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3)

                    # RGB_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                    # plt.imshow(RGB_img)

                    # split_file_name = l.split("/")

                    # if not os.path.isdir(f"TireLineDetection/data/processed/{split_file_name[-2]}/"):
                    #     os.mkdir(f"TireLineDetection/data/processed/{split_file_name[-2]}/")

                    # plt.savefig(f"TireLineDetection/data/processed/{split_file_name[-2]}/{split_file_name[-1]}")

                # Convert to gif and delete all images

        # with imageio.get_writer(f"TireLineDetection/data/processed/{split_file_name[-2]}/test.gif", mode="I") as writer:
        #     for filename in os.listdir(f"TireLineDetection/data/processed/{split_file_name[-2]}/"):
        #         image = imageio.imread(f"TireLineDetection/data/processed/{split_file_name[-2]}/{filename}")
        #         writer.append_data(image)

                    
                
                        
                        
                        
                        # data.append([row['xmin'], row['ymin'], row['xmax'], row['ymax']])
                        # labels.append(classes['names'][row["class"]])




            
            
            
        
        
    

    
    


