import cv2
import numpy as np
import os
import time
from datetime import datetime


def calibrate(cap, squaresX, squaresY, square_size, markerLength, dictionary='DICT_4X4_100',
              calibration_folder='Calibration-setup', min_corners=15):
    """
    Perform online calibration and save calibration data.

    Parameters:
    - cap (str or int): The device index or the video file path.
    - squaresX (int): Number of squares along the X-axis on the Charuco board.
    - squaresY (int): Number of squares along the Y-axis on the Charuco board.
    - square_size (float): The size of each square on the Charuco board (in meters).
    - markerLength (float): The size of the ArUco markers on the Charuco board (in meters).
    - dictionary (str): The type of ArUco dictionary to use.
    - frame_interval_calib (int): Interval between frames to use for calibration (unused in this standalone version).
    - save_every_n_frames (int): Interval between frames to save (unused in this standalone version).
    - calibration_folder (str): Folder to save calibration data and videos.
    - min_corners (int): Minimum number of corners for valid frame detection.
    """
    if not os.path.exists(calibration_folder):
        os.makedirs(calibration_folder)

    video_capture = cv2.VideoCapture(cap)
    all_charuco_corners = []
    all_charuco_ids = []

    countdown_start = 5
    countdown_end_time = time.time() + countdown_start
    calibration_and_recording_end_time = countdown_end_time + 10

    font = cv2.FONT_HERSHEY_SIMPLEX
    location = (50, 50)
    font_scale = 1
    font_color = (255, 0, 0)
    line_type = 2

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    calib_vidpath = os.path.join(calibration_folder, f'calibration_video_{timestamp}.avi')
    calib_filepath = os.path.join(calibration_folder, f'calibration_data_{timestamp}.npz')
    frame_width = int(video_capture.get(3))
    frame_height = int(video_capture.get(4))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(calib_vidpath, fourcc, fps, (frame_width, frame_height))

    aruco_dict = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dictionary))
    pattern_size = (squaresX, squaresY)
    board = cv2.aruco.CharucoBoard(pattern_size, square_size / 1000, markerLength / 1000,
                                   aruco_dict)

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        current_time = time.time()
        if current_time < countdown_end_time:
            remaining_time = int(countdown_end_time - current_time)
            cv2.putText(frame, f"Calibration & Recording starts in: {remaining_time}", location, font, font_scale,
                        font_color, line_type)
        elif current_time < calibration_and_recording_end_time:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict)
            if corners:
                ret, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(corners, ids, gray, board)
                if ret and len(charuco_corners) > min_corners:
                    all_charuco_corners.append(charuco_corners)
                    all_charuco_ids.append(charuco_ids)
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            remaining_time = int(calibration_and_recording_end_time - current_time)
            cv2.putText(frame, f"Recording & Calibration: {remaining_time}s", location, font, font_scale, font_color,
                        line_type)
        else:
            break

        cv2.imshow('Collecting Frames for Calibration & Recording', frame)
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    out.release()
    cv2.destroyAllWindows()

    if all_charuco_corners and all_charuco_ids:
        ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(all_charuco_corners, all_charuco_ids, board,
                                                                        gray.shape[::-1], None, None)
        np.savez(calib_filepath, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    print(f'Calibration saved into {calib_filepath}')

    return calib_filepath


class Transformation:
    def __init__(self, calib_path):
        with np.load(calib_path) as X:
            self.mtx, self.dist, self.rvecs, self.tvecs,  = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
        self.rotation_matrix = self.rvec_to_rotation_matrix(self.rvecs[0])
        self.transformation_matrix = self.construct_transformation_matrix(self.rotation_matrix, self.tvecs[0])

    def rvec_to_rotation_matrix(self, rvec):
        rotation_matrix, _ = cv2.Rodrigues(rvec)
        return rotation_matrix

    def construct_transformation_matrix(self, rotation_matrix, tvec):
        transformation_matrix = np.eye(4)
        transformation_matrix[:3, :3] = rotation_matrix
        transformation_matrix[:3, 3] = tvec.squeeze()
        return transformation_matrix

    def process_frame(self, frame):
        # Calculate the optimal new camera matrix
        h, w = frame.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w, h), 1, (w, h))

        # Undistort the frame
        undistorted_frame = cv2.undistort(frame, self.mtx, self.dist, None, new_camera_matrix)

        # Crop the undistorted frame based on the ROI
        x, y, w, h = roi
        undistorted_frame = undistorted_frame[y:y + h, x:x + w]
        return undistorted_frame

    def camera_to_robot_coordinate(self, pixel_x, pixel_y, depth):
        """

        :param pixel_x: x coordinates of the hands or robots
        :param pixel_y: y coordinates of the hands/robots
        :param depth: depth as obser

        :return:
        """
        # Convert pixel coordinates to camera coordinates using the intrinsic matrix
        point_in_camera = np.linalg.inv(self.mtx) @ np.array([pixel_x * depth, pixel_y * depth, depth, 1])

        # Apply the transformation matrix
        point_in_robot = self.transformation_matrix @ point_in_camera

        # Convert from homogeneous coordinates back to 3D
        point_in_robot_mm = point_in_robot[:3] / point_in_robot[3]
        #
        # Assuming the robot's unit is in millimeters and depth is in meters,
        # Convert the coordinates to millimeters if necessary
        # point_in_robot_mm = point_in_robot * 1000  # Convert from meters to millimeters

        return point_in_robot_mm


if __name__ == '__main__':
    squareX = 16
    squareY = 11
    square_size = 33
    markerLength = 26
    dictionary = 'DICT_4X4_100'
    # calibrate
    calibration_path = calibrate(0, squareX, squareY, square_size, markerLength, dictionary='DICT_4X4_100',
              calibration_folder='Calibration-setup', min_corners=15)

    # Perform undistortion/ correction
    # Compute Transformation
    # Convert to Robot coordinate


