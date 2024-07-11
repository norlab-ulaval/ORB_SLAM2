#!/bin/bash

### APRIL ###
exposure_time=16.0
experiment=forest_04-21-2023
file_name=backpack_2023-04-21-09-15-59

./Main/stereo/stereo_borealhdr Vocabulary/ORBvoc.txt Main/stereo/calib_files/BOREALHDR_april.yaml ../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/ ../data/$experiment/data_high_resolution/$file_name/camera_right/$exposure_time/

### SEPTEMBER ###
exposure_time=16.0
experiment=belair_09-27-2023
file_name=backpack_2023-09-27-13-29-22

# ./Main/stereo/stereo_borealhdr Vocabulary/ORBvoc.txt Main/stereo/calib_files/BOREALHDR_september_modified.yaml ../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/ ../data/$experiment/data_high_resolution/$file_name/camera_right/$exposure_time/