import cv2
import os


def display_image_pair(left_image_path, right_image_path, view_size=(800, 600)):
    # Load images
    left_image = cv2.imread(left_image_path)
    right_image = cv2.imread(right_image_path)

    # Resize images if necessary
    left_image = cv2.resize(left_image, view_size)
    right_image = cv2.resize(right_image, view_size)

    # Concatenate images horizontally
    image_pair = cv2.hconcat([left_image, right_image])

    # Create window to display images
    cv2.namedWindow('Image Pair', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image Pair', view_size[0] * 2, view_size[1])
    cv2.imshow('Image Pair', image_pair)


def navigate_image_pairs(left_image_directory, right_image_directory, view_size=(800, 600)):
    left_image_paths = [os.path.join(left_image_directory, f) for f in sorted(os.listdir(left_image_directory)) if
                        f.endswith('.png')]
    right_image_paths = [os.path.join(right_image_directory, f) for f in sorted(os.listdir(right_image_directory)) if
                         f.endswith('.png')]
    num_images = len(left_image_paths)
    current_index = 0

    display_image_pair(left_image_paths[current_index], right_image_paths[current_index], view_size)

    while True:
        key = cv2.waitKeyEx(0)  # Wait indefinitely for a key event

        if key == ord('q') or current_index >= num_images - 1:
            print("Quitting...")
            break
        elif key == 65363:  # Right arrow key
            current_index = min(current_index + 1, num_images - 1)
        elif key == 65361:  # Left arrow key
            current_index = max(current_index - 1, 0)
        else:
            continue

        display_image_pair(left_image_paths[current_index], right_image_paths[current_index], view_size)


# Example usage
if __name__ == "__main__":
    left_image_dir = '/home/qub-hri/Documents/QUBVisionData/RawData/CAM_UR/StereoCalibFrames'
    right_image_dir = '/home/qub-hri/Documents/QUBVisionData/RawData/CAM_UL/StereoCalibFrames'
    view_size = (800, 600)  # Adjust the view size as needed
    navigate_image_pairs(left_image_dir, right_image_dir, view_size)
