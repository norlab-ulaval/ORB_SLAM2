#!/bin/bash

### APRIL ###
exposure_time=8.0
experiment=forest_04-20-2023
file_name=backpack_2023-04-20-09-29-14

# ./Main/stereo_borealhdr_euroc Vocabulary/ORBvoc.txt Main/calib_files/BOREALHDR_april_low_resolution.yaml ../data/$experiment/data/$file_name/camera_left/$exposure_time/ ../data/$experiment/data/$file_name/camera_right/$exposure_time/ ../data/$experiment/data/$file_name/times_files/times_$exposure_time.txt 

### SEPTEMBER ###
exposure_time=4.0
experiment=belair_09-27-2023
file_name=backpack_2023-09-27-12-51-03

# september (do not use! Very bad)
# ./Main/stereo_borealhdr_euroc Vocabulary/ORBvoc.txt Main/calib_files/BOREALHDR_september_low_resolution.yaml ../data/$experiment/data/$file_name/camera_left/$exposure_time/ ../data/$experiment/data/$file_name/camera_right/$exposure_time/ ../data/$experiment/data/$file_name/times_$exposure_time.txt 

# september modified
./Main/stereo_borealhdr_euroc Vocabulary/ORBvoc.txt Main/calib_files/BOREALHDR_september_modified_low_resolution.yaml ../data/$experiment/data/$file_name/camera_left/$exposure_time/ ../data/$experiment/data/$file_name/camera_right/$exposure_time/ ../data/$experiment/data/$file_name/times_files/times_$exposure_time.txt 
