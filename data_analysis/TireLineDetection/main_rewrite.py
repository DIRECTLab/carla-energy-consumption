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
import imageio
from tqdm import tqdm
import copy
from ultralytics import YOLO



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
            if distance < least_distance and car_info[i][-1] > 350 and distance < 900 and abs(slope) < 0.8:
                least_distance = distance
                closest_car = car_info[i][2]
                closest_index = i



    return least_distance, closest_car, closest_index

def get_tire_positions(result, mask_num):  
    left_tire_outside = (-1, -1)
    left_tire_inside = (-1, -1)
    right_tire_outside = (-1, -1)
    right_tire_inside = (-1, -1)
    # Get the highest and lowest x for the masks
    # This will give us the positions that can be rescaled
    mask_locations = np.array(result.masks[mask_num].xyn[0])

    lowest = mask_locations.min(axis=0)
    highest = mask_locations.max(axis=0)

    # We can use this to find where to look
    start_x = int(lowest[0] * 640)
    start_y = int(highest[1] * 384) - 30
    end_x = int(highest[0] * 640)
    end_y = int(lowest[1] * 384) - 20
    halfway_x = (end_x + start_x) // 2
    
    
    # Start at the bottom of the image, which for the mask might be like a regular coord plane
    for y in range(start_y, end_y, -1):
        for x in range(start_x, halfway_x):
            if [x / 640, y / 384] in mask_locations:
                left_tire_outside = (int((x / 640) * 1920), int(((y + 30) / 384) * 1080))
                break
                # print(left_tire)
                # break
        
        for x in range(halfway_x, start_x, -1):
            if [x / 640, y / 384] in mask_locations and left_tire_inside == (-1, -1):
                left_tire_inside = (int((x / 640) * 1920), int(((y + 30) / 384) * 1080)) 
                break
                
        
        for x in range(end_x, halfway_x, -1):
            if [x / 640, y / 384] in mask_locations:
                right_tire_outside = (int((x / 640) * 1920), int(((y + 30) / 384) * 1080))
                break
                # print(right_tire)
        # for x in range(halfway_x, end_x):
        #     if [x / 640, y / 384] in mask_locations:
        #         right_tire_inside = (int((x / 640) * 1920), int((y / 384) * 1080))
        #         break
                
                
        if left_tire_outside != (-1, -1) and right_tire_outside != (-1, -1) and left_tire_inside != (-1, -1):
            break
        
    width_of_tires = abs(left_tire_outside[0] - left_tire_inside[0]) // 2
    right_tire = (right_tire_outside[0] - width_of_tires, right_tire_outside[1])
    
    return (left_tire_inside, right_tire)



if __name__ == "__main__":
    with open("yolo.yaml", "r") as f:
        classes = yaml.safe_load(f)
    print(classes)
    # yolo = torch.hub.load("ultralytics/yolov5", "yolov5l", pretrained=True)
    folders = os.listdir("data/frames")
    for folder_num, folder in enumerate(folders):
        yolo = YOLO('yolov8x-seg.pt')
        
        print(f"Beginning Folder: {folder}")
        good_anchor_point = (0, 0)
        good_anchor_point_times_seen = 0
        number_times_needed = 10
        anchor_point_threshold = 50.0


        images = [f"data/frames/{folder}/" + i for i in os.listdir(f"data/frames/{folder}")]
        # images = images[]

        dataloader = DataLoader(images, batch_size=1)
        print(len(images))

        loop = tqdm(dataloader)

        for index, i in enumerate(loop):
            data = []
            labels = []
            results = yolo.track(i, persist=True, verbose=False)
            # Left, right, middle, height
            car_info = []

            for result in results:
                centers_in_pixels = []
                cv_image = cv2.imread(result.path)
                black_box_image = copy.deepcopy(cv_image) 
                
                if result == None or result.boxes == None or result.boxes.id == None or result.boxes.cls == None:
                    break

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
                        (left_tire, right_tire) = get_tire_positions(result, j)
                        
                        
                        middle_x = (right_tire[0] + left_tire[0]) // 2
                        cv2.rectangle(cv_image, (left_tire[0], left_tire[1]), (left_tire[0] + 5, 0), (255, 255, 85), -1)  
                        cv2.rectangle(cv_image, (right_tire[0], right_tire[1]), (right_tire[0] + 5, 0), (255, 255, 85), -1)
                        cv2.rectangle(cv_image, (middle_x, (left_tire[1] + right_tire[1]) // 2), (middle_x, 0), (255, 0, 0), 2)
                        cv2.putText(cv_image, f"@{middle_x} pixels", (middle_x + 5, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)
                        cv2.putText(cv_image, f"ID: {tracking_ids[j]}", (middle_x + 5, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4)

                        centers_in_pixels.append((middle_x, (left_tire[1] + right_tire[1]) // 2))
                        car_info.append((left_tire, right_tire, (middle_x,  ((left_tire[1] + right_tire[1]) // 2)), h-y))



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
                            print("Switching anchor point")
            




                # Plot the approximate center
                # cv2.rectangle(cv_image, (middle_x, good_anchor_point[1]), (middle_x, 0), (255, 255, 255), 2)
                
                cv2.rectangle(cv_image, (good_anchor_point[0] - 5, good_anchor_point[1]), (good_anchor_point[0] + 5, good_anchor_point[1]), (0, 255, 0), 10)
                cv2.putText(cv_image, f"@{middle_x} pixels", (good_anchor_point[0] + 5, good_anchor_point[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                
                
                # ==================================================================================
                # Get Closest Car
                # ==================================================================================

                least_distance, closest_car, closest_index = get_closet_car(centers_in_pixels, good_anchor_point, car_info)


                if (least_distance < np.inf):
                # Now create the distance in pixels as rect on image
                    cv2.line(cv_image, (center_of_white_line), (centers_in_pixels[closest_index]), (255, 0, 255), 2)
                    cv2.putText(cv_image, f"{round(least_distance, 2)} pixels", (center_of_white_line[0] + 5, center_of_white_line[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3)

                RGB_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                plt.imshow(RGB_img)

                split_file_name = result.path.split("/")

                if not os.path.isdir(f"data/processed/{split_file_name[-2]}/"):
                    os.mkdir(f"data/processed/{split_file_name[-2]}/")

                plt.savefig(f"data/processed/{split_file_name[-2]}/{split_file_name[-1]}")
                plt.close()

                # Convert to gif
        with imageio.get_writer(f"data/processed/{split_file_name[-2]}/test.gif", mode="I") as writer:
            for filename in os.listdir(f"data/processed/{split_file_name[-2]}/"):
                image = imageio.imread(f"data/processed/{split_file_name[-2]}/{filename}")
                writer.append_data(image)

        
                    
                            
                            
                            
                            # data.append([row['xmin'], row['ymin'], row['xmax'], row['ymax']])
                        # labels.append(classes['names'][row["class"]])




            
            
            
            
            
        

        
        


