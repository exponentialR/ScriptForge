import cv2
import numpy as np
import glob


def rectify_stereo_images(imgL, img_R, calibration_left, calibration_right):
    # Extract calibration data
    cam_matrix_left, dist_coeffs_left = calibration_left['cam_matrix'], calibration_left['dist_coeffs']
    cam_matrix_right, dist_coeffs_right = calibration_right['cam_matrix'], calibration_right['dist_coeffs']
    rvecs_left, tvecs_left = calibration_left['rvecs'], calibration_left['tvecs']
    rvecs_right, tvecs_right = calibration_right['rvecs'], calibration_right['tvecs']

    # Compute rectification matrices and projection matrices
    R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(cam_matrix_left, dist_coeffs_left,
                                                               cam_matrix_right, dist_coeffs_right,
                                                               imgL.shape[::-1], rvecs_left, tvecs_left,
                                                               rvecs_right, tvecs_right,
                                                               flags=cv2.CALIB_ZERO_DISPARITY)

    # Compute rectification maps
    left_map1, left_map2 = cv2.initUndistortRectifyMap(cam_matrix_left, dist_coeffs_left, R1, P1,
                                                       imgL.shape[::-1], cv2.CV_16SC2)
    right_map1, right_map2 = cv2.initUndistortRectifyMap(cam_matrix_right, dist_coeffs_right, R2, P2,
                                                         img_R.shape[::-1], cv2.CV_16SC2)

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
