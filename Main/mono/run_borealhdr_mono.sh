#!/bin/bash

### APRIL ###
# exposure_time=4.0
# experiment=forest_04-21-2023
# file_name=backpack_2023-04-21-08-51-27

# ./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_april.yaml ../../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/

### July ###
exposure_time=4.0
experiment=campus_08-01-2024
file_name=backpack_2024-08-01-15-21-13

# # Bracketing
# ./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_august_01_left.yaml ../../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/ ./results/$file_name/orbslam2/mono/$exposure_time/

# Automatic exposure time
./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_august_01_right.yaml ../../data/$experiment/data_high_resolution/$file_name/camera_right/auto_exposure/ ../results/$file_name/orbslam2/mono/auto_exposure/

# # All brackets
# ./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_august_01_left.yaml ../../data/$experiment/data_high_resolution/$file_name/camera_left/all_brackets/ ../results/$file_name/orbslam2/mono/all_brackets/