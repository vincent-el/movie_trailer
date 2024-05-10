import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from moviepy.audio.fx.volumex import volumex
from moviepy.audio.fx.audio_fadeout import audio_fadeout
import re

def create_movie_clip(audio_folder, video_folder, output_file):
    # Function to sort filenames naturally (1, 2, 3...10, 11, 12...)
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

    # List of audio and video files sorted to ensure correct order
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.mp3')], key=natural_sort_key)
    video_files = sorted([f for f in os.listdir(video_folder) if f.endswith('.mp4')], key=natural_sort_key)

    # Ensure that the number of audio and video files are the same
    if len(audio_files) != len(video_files):
        raise ValueError("The number of audio and video files does not match.")

    clips = []
    # Create clips by combining corresponding audio and video files
    for audio_file, video_file in zip(audio_files, video_files):
        video_path = os.path.join(video_folder, video_file)
        audio_path = os.path.join(audio_folder, audio_file)

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        video_clip = video_clip.set_audio(audio_clip)

        clips.append(video_clip)
    
    final_clip = concatenate_videoclips(clips, method="compose")
    
    main_theme_audio = AudioFileClip("./assets/audio/main_theme.mp3")
    main_theme_audio = main_theme_audio.set_duration(final_clip.duration)
    main_theme_audio = volumex(main_theme_audio, 0.1)
    main_theme_audio = audio_fadeout(main_theme_audio, 10)
    final_clip = final_clip.set_audio(CompositeAudioClip([final_clip.audio, main_theme_audio]))
    
    final_clip.write_videofile(output_file, codec="libx264", fps=24)
