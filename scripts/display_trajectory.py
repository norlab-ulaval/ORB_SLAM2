import numpy as np
from scipy.spatial.transform import Rotation as R
import os

import matplotlib.pyplot as plt

def plot_orbslam_trajectory(file_path, ax_traj, color='k'):
    # Read the trajectory data from the file
    traj_name = file_path.split('/')[-1]
    data = np.loadtxt(file_path, delimiter=' ')

    # Extract the x, y, and z coordinates from the data
    x = data[:, 1]
    y = data[:, 2]
    z = data[:, 3]
    
    # NOTE: angle does not work since it is in the camera frame with Z in front
    # Convert the quaternion data to yaw angles
    quaternions = data[:, 4:]
    rotations = R.from_quat(quaternions)
    euler_angles = rotations.as_euler('zyx')
    
    # Not sure about yaw calculation, always get weird results
    yaw = np.unwrap(euler_angles[:, 2])
    dz = np.cos(yaw)
    dx = np.sin(yaw)
    
    # ax_traj.plot(yaw, color=color, label=traj_name)
    
    # Plot the trajectory
    # ax_traj.scatter(z, -x, color=color, label=traj_name)
    ax_traj.quiver(z[:-1], -x[:-1], dz[:-1], -dx[:-1], scale_units='xy', scale=2, width=0.01, angles='xy', color=color, label=traj_name)
    
def plot_icp_trajectory(file_path, ax_traj, color='k'):
    # Read the trajectory data from the file
    data = np.loadtxt(file_path, delimiter=',', skiprows=3)

    # Extract the x, y, and z coordinates from the data
    x = data[:, 1]
    y = data[:, 2]
    z = data[:, 3]
    
    # NOTE: angle does not work since it is in the camera frame with Z in front
    # Convert the quaternion data to yaw angles
    quaternions = data[:, 4:]
    rotations = R.from_quat(quaternions)
    euler_angles = rotations.as_euler('zyx')
    
    # Not sure about yaw calculation, always get weird results
    yaw = np.unwrap(euler_angles[:, 0])
    dx = np.cos(yaw)
    dy = np.sin(yaw)

    # Plot the trajectory
    # ax_traj.scatter(-x, -y, color=color, label="ICP Trajectory")
    ax_traj.quiver(-x[:-1], -y[:-1], -dx[:-1], -dy[:-1], scale_units='xy', scale=2, width=0.01, angles='xy', color=color, label="ICP Trajectory")
    

def main():
    # Example usage
    fig_traj = plt.figure()
    ax_traj = fig_traj.add_subplot(111)#, projection='3d')
    ax_traj.set_xlabel('X')
    ax_traj.set_ylabel('Y')
    ax_traj.set_title('ORBSLAM2 Trajectories')

    experiment_name = 'backpack_2023-04-21-09-15-59'
    files_names = os.listdir(f'results/{experiment_name}/orbslam2/no_loop/')
    files_names = sorted(files_names, key=lambda x: int(x.split('_')[-2].split('.')[0]))
    colors = plt.cm.plasma(np.linspace(0, 1, len(files_names)))
    for file, color in zip(files_names, colors):
        if file.endswith('CameraTrajectory.txt'):
            plot_orbslam_trajectory(f'results/{experiment_name}/orbslam2/no_loop/' + file, ax_traj, color=color)
    plot_icp_trajectory(f'results/{experiment_name}/icp/{experiment_name}_lidar.csv', ax_traj, color='r')
    plt.axis('equal')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()