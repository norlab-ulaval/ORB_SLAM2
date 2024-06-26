#!/bin/bash

### APRIL ###
exposure_time=4.0
experiment=forest_04-21-2023
file_name=backpack_2023-04-21-08-51-27

./Examples/Monocular/mono_euroc Vocabulary/ORBvoc.txt Main/calib_files/BOREALHDR_april.yaml ../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/ ../data/$experiment/data_high_resolution/$file_name/times_files/times_$exposure_time.txt 

### SEPTEMBER ###
exposure_time=8.0
experiment=belair_09-27-2023
file_name=backpack_2023-09-27-12-51-03

# ./Examples/Monocular/mono_euroc Vocabulary/ORBvoc.txt Main/calib_files/BOREALHDR_september_modified_low_resolution.yaml ../data/$experiment/data/$file_name/camera_left/$exposure_time/ ../data/$experiment/data/$file_name/times_files/times_$exposure_time.txt 


### WARTHOG ###
experiment=warthog_2024-06-13_10-35-59

# ./Examples/Monocular/mono_euroc Vocabulary/ORBvoc.txt Main/calib_files/WARTHOG.yaml ../data/$experiment/rectified/camera_left ../data/$experiment/rectified/times.txt 
