import cv2
import yaml
import numpy as np
import os

def display_rectification(img_left, img_right, stereo_map_left, stereo_map_right, shape):

    img_left_rect = cv2.remap(img_left, stereo_map_left[0], stereo_map_left[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    img_right_rect = cv2.remap(img_right, stereo_map_right[0], stereo_map_right[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    
    img_left = cv2.cvtColor(img_left, cv2.COLOR_GRAY2BGR)
    img_right = cv2.cvtColor(img_right, cv2.COLOR_GRAY2BGR)
    img_left_rect_color = cv2.cvtColor(img_left_rect, cv2.COLOR_GRAY2BGR)
    img_right_rect_color = cv2.cvtColor(img_right_rect, cv2.COLOR_GRAY2BGR)
    
    for i in range(0, shape[1], 100):
        cv2.line(img_left_rect_color, (0, i), (shape[0], i), (0, 0, 255), 1)
        cv2.line(img_right_rect_color, (0, i), (shape[0], i), (0, 0, 255), 1)

    combined_image = np.hstack([img_left, img_right])
    combined_image_rect = np.hstack([img_left_rect_color, img_right_rect_color])
    combined_image_final = np.vstack([combined_image, combined_image_rect])
    combined_image_final = cv2.resize(combined_image_final, (0,0), fx=0.4, fy=0.4)
    cv2.imshow('Side by Side Images', combined_image_final)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return

EXPERIMENTS = "april" # "april" or "september

if EXPERIMENTS == "april":
    calib = yaml.safe_load(open("scripts/calib_files_python/BOREALHDR_april.yaml", 'r'))
elif EXPERIMENTS == "september":
    calib = yaml.safe_load(open("scripts/calib_files_python/BOREALHDR_september.yaml", 'r'))
elif EXPERIMENTS == "september_modified":
    calib = yaml.safe_load(open("scripts/calib_files_python/BOREALHDR_september_modified.yaml", 'r'))
elif EXPERIMENTS == "warthog":
    calib = yaml.safe_load(open("scripts/calib_files_python/WARTHOG.yaml", 'r'))
elif EXPERIMENTS == "euroc":
    calib = yaml.safe_load(open("scripts/calib_files_python/EuRoC.yaml", 'r'))

K_left = np.array(calib['LEFT.K']['data']).reshape((3, 3))
K_right = np.array(calib['RIGHT.K']['data']).reshape((3, 3))
distL = np.array(calib['LEFT.D']['data'])
distR = np.array(calib['RIGHT.D']['data'])
rectL = np.array(calib['LEFT.R']['data']).reshape((3, 3))
rectR = np.array(calib['RIGHT.R']['data']).reshape((3, 3))
P_left = np.array(calib['LEFT.P']['data']).reshape((3, 4))
P_right = np.array(calib['RIGHT.P']['data']).reshape((3, 4))
shape = (calib['LEFT.width'], calib['LEFT.height'])

stereo_map_left = cv2.initUndistortRectifyMap(K_left, distL, rectL, P_left, shape, cv2.CV_16SC2)
stereo_map_right = cv2.initUndistortRectifyMap(K_right, distR, rectR, P_right, shape, cv2.CV_16SC2)

if EXPERIMENTS == "april":
    for file in os.listdir("../data/forest_04-21-2023/data_high_resolution/backpack_2023-04-21-08-51-27/camera_left/8.0"):
        img_left = cv2.imread(f"../data/forest_04-21-2023/data_high_resolution/backpack_2023-04-21-08-51-27/camera_left/8.0/{file}", cv2.IMREAD_ANYDEPTH)
        img_right = cv2.imread(f"../data/forest_04-21-2023/data_high_resolution/backpack_2023-04-21-08-51-27/camera_right/8.0/{file}", cv2.IMREAD_ANYDEPTH)

        img_left = (img_left/16.0).astype(np.uint8)
        img_right = (img_right/16.0).astype(np.uint8)
        display_rectification(img_left, img_right, stereo_map_left, stereo_map_right, shape)
        
elif EXPERIMENTS == "september" or EXPERIMENTS == "september_modified":
    for file in os.listdir("../data/belair_09-27-2023/data_high_resolution/backpack_2023-09-27-12-46-32/camera_left/8.0"):
        img_left = cv2.imread(f"../data/belair_09-27-2023/data_high_resolution/backpack_2023-09-27-12-46-32/camera_left/8.0/{file}", cv2.IMREAD_ANYDEPTH)
        img_right = cv2.imread(f"../data/belair_09-27-2023/data_high_resolution/backpack_2023-09-27-12-46-32/camera_right/8.0/{file}", cv2.IMREAD_ANYDEPTH)

        img_left = (img_left/16.0).astype(np.uint8)
        img_right = (img_right/16.0).astype(np.uint8)
        display_rectification(img_left, img_right, stereo_map_left, stereo_map_right, shape)
            
elif EXPERIMENTS == "warthog":
    for file in os.listdir("../data_examples/warthog_2024-06-13_10-35-59/camera_left"):
        img_left = cv2.imread(f"../data_examples/warthog_2024-06-13_10-35-59/camera_left/{file}", cv2.IMREAD_ANYDEPTH)
        img_right = cv2.imread(f"../data_examples/warthog_2024-06-13_10-35-59/camera_right/{file}", cv2.IMREAD_ANYDEPTH)

        display_rectification(img_left, img_right, stereo_map_left, stereo_map_right, shape)
        
elif EXPERIMENTS == "euroc":
    for file in sorted(os.listdir("../data_examples/MH_03_medium/mav0/cam0/data/")):
        img_left = cv2.imread(f"../data_examples/MH_03_medium/mav0/cam0/data/{file}", cv2.IMREAD_ANYDEPTH)
        img_right = cv2.imread(f"../data_examples/MH_03_medium/mav0/cam1/data/{file}", cv2.IMREAD_ANYDEPTH)

        display_rectification(img_left, img_right, stereo_map_left, stereo_map_right, shape)