from moviepy.editor import VideoFileClip, AudioFileClip
from pathlib import Path


def add_variable_audio(video_path: str = None, long_audio_path: str = None, output_video_directory: str = None):
    """
    Adds audio track to a video file with variable length
    """
    video_clip = VideoFileClip(video_path)
    long_audio_clip = AudioFileClip(long_audio_path)

    trimmed_audio_clip = long_audio_clip.subclip(0, video_clip.duration)

    final_video_clip = video_clip.set_audio(trimmed_audio_clip)

    final_video_clip.write_videofile(output_video_directory, codec='libx264', audio_codec='aac')

    return output_video_directory


if __name__ == '__main__':
    video_path_use = 'GX010749_CC.avi'
    audio_path = 'town-for-two-168888.mp3'
    output_video = 'OutputVideo.mp4'
    video_out = add_variable_audio(video_path_use, audio_path, output_video)
