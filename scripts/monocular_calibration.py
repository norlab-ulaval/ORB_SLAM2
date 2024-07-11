import numpy as np
import cv2 as cv
import glob
import yaml
 
def camera_calibration(file_path, rows, columns, size_square, visualize=False):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((rows*columns,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)
    objp = objp*size_square

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    for fname in sorted(glob.glob(file_path + '/*.png')):
        img = cv.imread(fname)
        width, height = img.shape[:2]
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (rows,columns), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            print(fname)
            objpoints.append(objp)

            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            if visualize:
                cv.drawChessboardCorners(img, (rows,columns), corners2, ret)
                cv.imshow(fname, img)
                cv.waitKey(0)
                cv.destroyAllWindows()
                
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        mean_error += error
    reprojection_error = mean_error/len(objpoints)
 
    print("#####################################################")
    print(f"Total error of reprojected points: {reprojection_error}")
    print("#####################################################")
    
    save_calibration(file_path, width, height, mtx, dist, reprojection_error)
    return

def save_calibration(path, width, height, mtx, dist, reprojection_error):
    calib_dic = {
        "reprojection_error": reprojection_error,
        "image_width": width,
        "image_heigh": height,
        "camera_matrix": {
            "rows": 3,
            "cols": 3,
            "data": mtx.ravel().tolist(),
        },
        "distortion_coefficients": {
            "rows": 1,
            "cols": 5,
            "data": dist.ravel().tolist(),
        }
    }
    
    with open(f"{path}/manual_calib_file.yaml", 'w') as file:
        yaml.dump(calib_dic, file, default_flow_style=None, sort_keys=False)
    return

def main():
    # Parameters
    # file_path = "scripts/data_calibration/11-09-2023_calibrationdata_camera2/"
    file_path = "scripts/data_calibration/20-06-2024_calibration_stereo/LEFT"
    rows = 7
    columns = 6
    # size_square = 0.0228
    size_square = 0.1
    
    camera_calibration(file_path, rows, columns, size_square, visualize=False)
    return

if __name__ == "__main__":
    main()