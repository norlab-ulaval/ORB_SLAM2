#!/bin/bash

### APRIL ###
exposure_time=4.0
experiment=forest_04-21-2023
file_name=backpack_2023-04-21-08-51-27

./Main/mono/mono_borealhdr Vocabulary/ORBvoc.txt Main/mono/calib_files/BOREALHDR_april.yaml ../data/$experiment/data_high_resolution/$file_name/camera_left/$exposure_time/