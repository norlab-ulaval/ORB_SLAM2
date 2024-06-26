import os

# exposure_time = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
# experiment = "forest_04-21-2023"
# file_name = "backpack_2023-04-21-09-31-09"


# for exposure in exposure_time:
#     # Specify the folder path
#     folder_path = f"/home/user/data/{experiment}/data/{file_name}/camera_right/{exposure}/"

#     # Get the filenames in the folder
#     filenames = sorted(os.listdir(folder_path))
#     init_time = filenames[0].split('.')[0]

#     # Create a text file to write the filenames
#     output_file = f'/home/user/data/{experiment}/data/{file_name}/times_files/times_{exposure}.txt'
#     # Create the folder if it does not exist
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)

#     with open(output_file, 'w') as file:
#         # Write each filename to a new line in the text file
#         for filename in filenames:
#             time = int(filename.split('.')[0]) - int(init_time)
#             file.write(filename.split('.')[0] + '\n')
            
experiment = "warthog_2024-06-13_10-35-59"

# Specify the folder path
folder_path = f"/home/user/data_examples/{experiment}/rectified/camera_left/"

# Get the filenames in the folder
filenames = sorted(os.listdir(folder_path))
init_time = filenames[0].split('.')[0]

# Create a text file to write the filenames
output_file = f'/home/user/data_examples/{experiment}/rectified/times.txt'
# Create the folder if it does not exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as file:
    # Write each filename to a new line in the text file
    for filename in filenames:
        time = int(filename.split('.')[0]) - int(init_time)
        file.write(filename.split('.')[0] + '\n')