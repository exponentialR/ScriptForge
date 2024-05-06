import cv2
from pathlib import Path
import os
from tqdm import tqdm

OUT_DIR = 'before_calibration'


def extract_frame(video_path: str, output_folder: str = None, frame_interval: int = 10):
    """
    Extract frames from a video.
    """
    video_name = Path(video_path).stem
    output_folder = Path(output_folder)

    if output_folder is None:
        output_folder = OUT_DIR + video_name

    output_folder.mkdir(parents=True, exist_ok=True) if not os.path.exists(output_folder) else print(
        f'Output Folder already exist')

    print(f'Frames will be saved in {output_folder}')

    video_capture = cv2.VideoCapture(str(video_path))
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0
    pgbar = tqdm(total=total_frames, desc=f'Extracting Frames from Video {video_name}', unit='frame')

    while True:
        try:
            success, frame = video_capture.read()
            if not success:
                break

            if count % frame_interval == 0:
                frame_name = f'{video_name}_{count}.jpg'
                cv2.imwrite(str(output_folder / frame_name), frame)
                pgbar.update(frame_interval)
            count += 1

        except Exception as e:
            print(f"Error processing frame {count}: {e}")

    video_capture.release()
    pgbar.close()


if __name__ == '__main__':
    camera_views = ['CAM_UL', 'CAM_UR', 'CAM_LL', 'CAM_LR', 'CAM_AV']
    for participants_id in range(3, 11):
        for camera_view in camera_views:
            if participants_id == 3:
                task = 'BRIDGE_AS'
            elif participants_id == 4:
                task = 'TOWER_HO'
            elif participants_id == 10:
                task = 'TOWER_MS'
            else:
                continue
            video_path = f'/media/iamshri/Seagate/QUB-PHEOVision/p{participants_id:02d}/{camera_view}/{task}.mp4'
            output_folder = f'/media/iamshri/Seagate/QUB-PHEOVision/extracted-frames/p{participants_id:02d}/{camera_view}'
            extract_frame(video_path, output_folder)
