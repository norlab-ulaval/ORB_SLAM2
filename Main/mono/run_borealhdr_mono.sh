#!/bin/bash

### APRIL ###
# exposure_time=4.0
# experiment=forest_04-21-2023
# file_name=backpack_2023-04-21-08-51-27

# ./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_april.yaml ../../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/

### July ###
exposure_time=4.0
experiment=campus_07-22-2024
file_name=backpack_2024-07-22-14-07-23

# # Bracketing
# ./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_july_left.yaml ../../../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/

# Automatic exposure time
./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_july_right.yaml ../../data/$experiment/data_high_resolution/$file_name/camera_right/ ../results/$file_name/orbslam2/mono/auto_exposure/