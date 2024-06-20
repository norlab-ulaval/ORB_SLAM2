import cv2
import yaml
import numpy as np
import os

EXPERIMENTS = "september_modified" # "april" or "september

if EXPERIMENTS == "april":
    calib = yaml.safe_load(open("scripts/calib_files_python/BOREALHDR_april_low_resolution.yaml", 'r'))
elif EXPERIMENTS == "september":
    calib = yaml.safe_load(open("scripts/calib_files_python/BOREALHDR_september_low_resolution.yaml", 'r'))
elif EXPERIMENTS == "september_modified":
    calib = yaml.safe_load(open("scripts/calib_files_python/BOREALHDR_september_modified_low_resolution.yaml", 'r'))

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
    for file in os.listdir("../data/forest_04-20-2023/forest_04-20-2023/backpack_2023-04-20-09-29-14/camera_left/8.0"):
        img_left = cv2.imread(f"../data/forest_04-20-2023/forest_04-20-2023/backpack_2023-04-20-09-29-14/camera_left/8.0/{file}", cv2.IMREAD_ANYDEPTH)
        img_right = cv2.imread(f"../data/forest_04-20-2023/forest_04-20-2023/backpack_2023-04-20-09-29-14/camera_right/8.0/{file}", cv2.IMREAD_ANYDEPTH)

        img_left = (img_left/16.0).astype(np.uint8)
        img_right = (img_right/16.0).astype(np.uint8)

        img_left = cv2.remap(img_left, stereo_map_left[0], stereo_map_left[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        img_right = cv2.remap(img_right, stereo_map_right[0], stereo_map_right[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        img_left[50,:], img_right[50,:] = 0, 0

        combined_image = np.hstack([img_left, img_right])
        cv2.imshow('Side by Side Images', combined_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
elif EXPERIMENTS == "september" or EXPERIMENTS == "september_modified":
    for file in os.listdir("../data/belair_09-27-2023/belair_09-27-2023/backpack_2023-09-27-12-46-32/camera_left/8.0"):
            img_left = cv2.imread(f"../data/belair_09-27-2023/belair_09-27-2023/backpack_2023-09-27-12-46-32/camera_left/8.0/{file}", cv2.IMREAD_ANYDEPTH)
            img_right = cv2.imread(f"../data/belair_09-27-2023/belair_09-27-2023/backpack_2023-09-27-12-46-32/camera_right/8.0/{file}", cv2.IMREAD_ANYDEPTH)

            img_left = (img_left/16.0).astype(np.uint8)
            img_right = (img_right/16.0).astype(np.uint8)

            img_left = cv2.remap(img_left, stereo_map_left[0], stereo_map_left[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
            img_right = cv2.remap(img_right, stereo_map_right[0], stereo_map_right[1], cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
            img_left[50,:], img_right[50,:] = 0, 0

            combined_image = np.hstack([img_left, img_right])
            cv2.imshow('Side by Side Images', combined_image)
            cv2.waitKey(500)
            # cv2.destroyAllWindows()