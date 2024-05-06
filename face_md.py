import mediapipe as mp
import cv2
import numpy as np


# Use OpenCV’s VideoCapture to start capturing from the webcam.
cap = cv2.VideoCapture(0)
# Create a loop to read the latest frame from the camera using VideoCapture#read()
while True:
    # Read the frame from the camera
    ret, frame = cap.read()
    # Convert the received from OpenCV frame to a MediaPipe’s Image object.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_frame_from_opencv)

    # Display the frame
    cv2.imshow('Frame', frame)
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Convert the frame received from OpenCV to a MediaPipe’s Image object.
