import os.path

from moviepy.editor import VideoFileClip, AudioFileClip
from pathlib import Path
from pydub import AudioSegment


def check_decibel(audio_):
    average_loudness = audio_.dBFS
    peak_loudness = max(audio_.max_dBFS, audio_.max_dBFS)
    print(f"Average Loudness: {average_loudness} dBFS")
    print(f"Peak Loudness: {peak_loudness} dBFS")
    return average_loudness


def reduce_volume(audio_path: str=None, volume_reduction_dB:float=10.0, loudness_threshold:int=-20, output_audio_path:str=None):
    audio = AudioSegment.from_file(audio_path)
    average_loudness = check_decibel(audio)
    if average_loudness > loudness_threshold:
        print(f"Average loudness of {average_loudness} dBFS exceeds the threshold of {loudness_threshold} dBFS. Reducing volume by {volume_reduction_dB} dB.")
        audio = audio - volume_reduction_dB
    else:
        print(f"Average loudness of {average_loudness} dBFS is within acceptable range. No volume adjustment needed.")

    audio.export(output_audio_path, format='mp3')
    return f'Output audio reduced by {volume_reduction_dB} Decibel.\n Please check {output_audio_path} for output Audio'


def add_variable_audio(video_path: str = None, long_audio_path: str = None, output_video_directory: str = None):
    video_clip = VideoFileClip(video_path)
    long_audio_clip = AudioFileClip(long_audio_path)

    trimmed_audio_clip = long_audio_clip.subclip(0, video_clip.duration)

    final_video_clip = video_clip.set_audio(trimmed_audio_clip)

    final_video_clip.write_videofile(output_video_directory, codec='libx264', audio_codec='aac')

    return output_video_directory


if __name__ == '__main__':
    video_path_use = 'src/videos/CAM_LL/GX010749_CC.avi'
    audio_path = 'src/audio/town-for-two-168888.mp3'
    output_audio_path = os.path.basename(audio_path)
    output_audio_path = f'reduced_dB_{output_audio_path}'
    print(reduce_volume(audio_path, output_audio_path=output_audio_path)) # Only add this if the audio is too loud
    output_video = 'OutputVideo.mp4'
    video_out = add_variable_audio(video_path_use, audio_path, output_video)
