import cv2
import numpy as np
import glob


def rectify_stereo_images(imgL, img_R, calibration_left, calibration_right):
    # Extract calibration data
    cam_matrix_left, dist_coeffs_left = calibration_left['mtx'], calibration_left['dist']
    cam_matrix_right, dist_coeffs_right = calibration_right['mtx'], calibration_right['dist']
    rvecs_left, tvecs_left = calibration_left['rvecs'], calibration_left['tvecs']
    rvecs_right, tvecs_right = calibration_right['rvecs'], calibration_right['tvecs']

    # Print calibration parameters for left camera
    print("Left Camera Calibration Parameters:")
    print("Len of Camera Matrix (mtx):", len(calibration_left['mtx']))
    print("Len of Distortion Coefficients (dist):", len(calibration_left['dist']))
    print("Len of Rotation Vectors (rvecs):", len(calibration_left['rvecs']))
    print("Len of Translation Vectors (tvecs):", len(calibration_left['tvecs']))

    # Print calibration parameters for right camera
    print("Right Camera Calibration Parameters:")
    print("Len of Camera Matrix (mtx):", len(calibration_right['mtx']))
    print("Len of Distortion Coefficients (dist):", len(calibration_right['dist']))
    print("Len of Rotation Vectors (rvecs):", len(calibration_right['rvecs']))
    print("Len of Translation Vectors (tvecs):", len(calibration_right['tvecs']))

    # Get image dimensions
    left_height, left_width, _ = imgL.shape
    right_height, right_width, _ = img_R.shape

    # Compute rectification matrices and projection matrices
    R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(cam_matrix_left, dist_coeffs_left,
                                                               cam_matrix_right, dist_coeffs_right,
                                                               (left_width, left_height), rvecs_left, tvecs_left,
                                                               rvecs_right, tvecs_right,
                                                               flags=cv2.RANSAC)

    # Compute rectification maps
    left_map1, left_map2 = cv2.initUndistortRectifyMap(cam_matrix_left, dist_coeffs_left, R1, P1,
                                                       (left_width, left_height), cv2.CV_16SC2)
    right_map1, right_map2 = cv2.initUndistortRectifyMap(cam_matrix_right, dist_coeffs_right, R2, P2,
                                                         (right_width, right_height), cv2.CV_16SC2)

    # Remap the images
    imgL_rectified = cv2.remap(imgL, left_map1, left_map2, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    img_R_rectified = cv2.remap(img_R, right_map1, right_map2, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

    return imgL_rectified, img_R_rectified, Q


# function for depth map
def depth_map(imgL, imgR, Q):
    # SGBM Parameters
    window_size = 3
    left_matcher = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=160,
        blockSize=5,
        P1=8 * 3 * window_size ** 2,
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)
    # WLS FILTER Parameters
    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0
    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)
    displ = left_matcher.compute(imgL, imgR)  # .astype(np.float32)/16
    dispr = right_matcher.compute(imgR, imgL)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)
    filtered_disp = wls_filter.filter(displ, imgL, None, dispr)  # important to put "imgL" here!!!
    filtered_disp = cv2.normalize(src=filtered_disp, dst=filtered_disp, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    filtered_disp = np.uint8(filtered_disp)

    # Convert disparity map to depth map
    depth_map = cv2.reprojectImageTo3D(filtered_disp, Q)

    return depth_map


# function to visualize depth map
def visualize_depth_map(depth_map):
    # Normalize depth values for visualization
    min_depth = np.min(depth_map)
    max_depth = np.max(depth_map)
    normalized_depth_map = (depth_map - min_depth) / (max_depth - min_depth)

    # Apply colormap (Jet colormap is commonly used for depth visualization)
    depth_colormap = cv2.applyColorMap((normalized_depth_map * 255).astype(np.uint8), cv2.COLORMAP_JET)

    # Optionally, apply gamma correction for better visualization
    gamma = 0.6
    depth_colormap_corrected = np.clip(((depth_colormap / 255) ** (1 / gamma)) * 255, 0, 255).astype(np.uint8)

    return depth_colormap_corrected


if __name__ == '__main__':
    # Load calibration data
    calibration_left = np.load('/media/iamshri/Seagate/QUB-PHEOVision/p01/CAM_LL/calib_param_CALIBRATION.npz')
    calibration_right = np.load('/media/iamshri/Seagate/QUB-PHEOVision/p01/CAM_LR/calib_param_CALIBRATION.npz')

    # Load stereo images
    imgL = cv2.imread('/media/iamshri/Seagate/QUB-PHEOVision/p01/CAM_LL/extracted-frames/BIAH_BS_0.jpg')
    imgR = cv2.imread('/media/iamshri/Seagate/QUB-PHEOVision/p01/CAM_LR/extracted-frames/BIAH_BS_0.jpg')

    # Rectify stereo images
    imgL_rectified, img_R_rectified, Q = rectify_stereo_images(imgL, imgR, calibration_left, calibration_right)

    # Compute depth map
    depth_map = depth_map(imgL_rectified, img_R_rectified, Q)

    # Visualize depth map
    depth_map_visualized = visualize_depth_map(depth_map)

    # Display depth map
    cv2.imshow('Depth Map', depth_map_visualized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
