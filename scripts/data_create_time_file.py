import os

exposure_time = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
experiment = "belair_09-27-2023"
file_name = "backpack_2023-09-27-12-46-32"


for exposure in exposure_time:
    # Specify the folder path
    folder_path = f"/home/user/data/{experiment}/data_high_resolution/{file_name}/camera_left/{exposure}/"

    # Get the filenames in the folder
    filenames = sorted(os.listdir(folder_path))
    init_time = filenames[0].split('.')[0]

    # Create a text file to write the filenames
    output_file = f'/home/user/data/{experiment}/data_high_resolution/{file_name}/times_files/times_{exposure}.txt'
    # Create the folder if it does not exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as file:
        # Write each filename to a new line in the text file
        for filename in filenames:
            time = int(filename.split('.')[0]) - int(init_time)
            file.write(filename.split('.')[0] + '\n')