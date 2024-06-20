#!/bin/bash

### APRIL ###
exposure_time=4.0
experiment=forest_04-21-2023
file_name=backpack_2023-04-21-08-51-27

./Main/stereo_borealhdr_euroc Vocabulary/ORBvoc.txt Main/calib_files/BOREALHDR_april.yaml ../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/ ../data/$experiment/data_high_resolution/$file_name/camera_right/$exposure_time/ ../data/$experiment/data_high_resolution/$file_name/times_files/times_$exposure_time.txt 

### SEPTEMBER ###
exposure_time=4.0
experiment=belair_09-27-2023
file_name=backpack_2023-09-27-12-46-32

# september modified
# ./Main/stereo_borealhdr_euroc Vocabulary/ORBvoc.txt Main/calib_files/BOREALHDR_september_modified.yaml ../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/ ../data/$experiment/data_high_resolution/$file_name/camera_right/$exposure_time/ ../data/$experiment/data_high_resolution/$file_name/times_files/times_$exposure_time.txt 
