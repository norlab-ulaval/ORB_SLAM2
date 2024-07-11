import numpy as np
import cv2
import glob
import argparse
from tqdm import tqdm
import yaml


class StereoCalibration(object):
    def __init__(self, filepath, rows, columns, size_square):
        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS +
                         cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.criteria_cal = (cv2.TERM_CRITERIA_EPS +
                             cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
        self.rows = rows
        self.columns = columns
        self.size_square = size_square
        
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((self.rows*self.columns, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.rows, 0:self.columns].T.reshape(-1, 2)
        self.objp = self.objp*self.size_square

        # Arrays to store object points and image points from all the images.
        self.objpoints = []  # 3d point in real world space
        self.imgpoints_l = []  # 2d points in image plane.
        self.imgpoints_r = []  # 2d points in image plane.

        self.cal_path = filepath
        self.read_images(self.cal_path)

    def read_images(self, cal_path):
        print("Extracting chessboard corners...")
        images_right = sorted(glob.glob(cal_path + 'RIGHT/*.png'))
        images_left = sorted(glob.glob(cal_path + 'LEFT/*.png'))

        for i, fname in tqdm(enumerate(images_right)):
            gray_l = cv2.imread(images_left[i], cv2.IMREAD_GRAYSCALE)
            gray_r = cv2.imread(images_right[i], cv2.IMREAD_GRAYSCALE)

            # Find the chess board corners
            ret_l, corners_l = cv2.findChessboardCorners(gray_l, (self.rows, self.columns), None)
            ret_r, corners_r = cv2.findChessboardCorners(gray_r, (self.rows, self.columns), None)


            if ret_l is True and ret_r is True:
                # If found, add object points, image points (after refining them)
                self.objpoints.append(self.objp)
                rt = cv2.cornerSubPix(gray_l, corners_l, (11, 11),
                                      (-1, -1), self.criteria)
                self.imgpoints_l.append(corners_l)

                # Draw and display the corners
                ret_l = cv2.drawChessboardCorners(gray_l, (self.rows, self.columns),
                                                  corners_l, ret_l)
                # cv2.imshow(images_left[i], gray_l)
                # cv2.waitKey(500)
                # cv2.destroyAllWindows()

            # if ret_l is True and ret_r is True:
                rt = cv2.cornerSubPix(gray_r, corners_r, (11, 11),
                                      (-1, -1), self.criteria)
                self.imgpoints_r.append(corners_r)

                # Draw and display the corners
                ret_r = cv2.drawChessboardCorners(gray_r, (self.rows, self.columns),
                                                  corners_r, ret_r)
                # cv2.imshow(images_right[i], gray_r)
                # cv2.waitKey(500)
                # cv2.destroyAllWindows()
            self.img_shape = gray_l.shape[::-1]

        rt, self.M1, self.d1, self.r1, self.t1 = cv2.calibrateCamera(self.objpoints, self.imgpoints_l, self.img_shape, None, None)
        rt, self.M2, self.d2, self.r2, self.t2 = cv2.calibrateCamera(self.objpoints, self.imgpoints_r, self.img_shape, None, None)

        # self.camera_model = self.stereo_calibrate(img_shape)

    def extract_intrinsics(self, file):
        with open(file, 'r') as f:
            intrinsics = yaml.safe_load(f)   
        return intrinsics["camera_matrix"]["data"], intrinsics["distortion_coefficients"]["data"]
    
    def set_intrinsics(self, which_cam, camera_matrix, dist_coeffs):
        if which_cam == "left":
            self.M1 = np.array(camera_matrix).reshape(3, 3)
            self.d1 = np.array(dist_coeffs)
        elif which_cam == "right":
            self.M2 = np.array(camera_matrix).reshape(3, 3)
            self.d2 = np.array(dist_coeffs)
    
    def stereo_calibrate(self):
        # flags = 0
        flags = cv2.CALIB_FIX_INTRINSIC
        # flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
        # flags = cv2.CALIB_USE_INTRINSIC_GUESS
        # flags |= cv2.CALIB_FIX_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_ASPECT_RATIO
        # flags |= cv2.CALIB_ZERO_TANGENT_DIST
        # flags |= cv2.CALIB_RATIONAL_MODEL
        # flags |= cv2.CALIB_SAME_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_K3
        # flags |= cv2.CALIB_FIX_K4
        # flags |= cv2.CALIB_FIX_K5

        stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                                cv2.TERM_CRITERIA_EPS, 100, 1e-5)
        
        print(f"Camera matrix left:\n{self.M1}")
        print(f"Camera matrix right:\n{self.M2}")
        ret, M1, d1, M2, d2, R, T, E, F = cv2.stereoCalibrate(
            self.objpoints, self.imgpoints_l,
            self.imgpoints_r, self.M1, self.d1, self.M2,
            self.d2, self.img_shape,
            criteria=stereocalib_criteria, flags=flags)
        
        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(M1, d1, M2, d2, self.img_shape, R, T, flags=cv2.CALIB_ZERO_DISPARITY, alpha=0)
        
        self.camera_model = {
            'K1': M1.ravel().tolist(),
            'D1': d1.ravel().tolist(),
            'R1': R1.ravel().tolist(),
            'P1': P1.ravel().tolist(),
            'K2': M2.ravel().tolist(),
            'D2': d2.ravel().tolist(),
            'R2': R2.ravel().tolist(),
            'P2': P2.ravel().tolist(),
        }

        cv2.destroyAllWindows()
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file_path', help='(String) Filepath')
    parser.add_argument('-i','--intrinsics', help='(Bool) If want to use already calculated intrinsic parameters', default=False)
    args = parser.parse_args()
    
    # Read stereo images
    cal_data = StereoCalibration(args.file_path, rows=7, columns=6, size_square=0.1)
    # cal_data = StereoCalibration(args.file_path, rows=10, columns=7, size_square=0.0228)
    
    # Fetch already calculated intrinsic parameters
    if args.intrinsics:
        print("Using already calculated intrinsic parameters")
        camera_left_calib_file = "scripts/data_calibration/11-09-2023_calibrationdata_camera1/manual_calib_file.yaml"
        camera_left_k, camera_left_d = cal_data.extract_intrinsics(camera_left_calib_file)
        cal_data.set_intrinsics("left", camera_left_k, camera_left_d)
        camera_right_calib_file = "scripts/data_calibration/11-09-2023_calibrationdata_camera2/manual_calib_file.yaml"
        camera_right_k, camera_right_d = cal_data.extract_intrinsics(camera_right_calib_file)
        cal_data.set_intrinsics("right", camera_right_k, camera_right_d)
    
    # Stereo calibration
    camera_model = cal_data.stereo_calibrate()
    
    with open('manual_calib_stereo.yaml', 'w') as f:
        yaml.dump(cal_data.camera_model, f, default_flow_style=None, sort_keys=False)
        print("Calibration data saved to manual_calib_stereo.yaml")