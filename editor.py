import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def create_movie_clip(audio_folder, video_folder, output_file):
    # List of audio and video files sorted to ensure correct order
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.mp3')])
    video_files = sorted([f for f in os.listdir(video_folder) if f.endswith('.mp4')])

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

        # Set the audio of the video clip
        video_clip = video_clip.set_audio(audio_clip)

        clips.append(video_clip)

    # Concatenate all clips into one final clip
    final_clip = concatenate_videoclips(clips, method="compose")

    # Write the result to a file
    final_clip.write_videofile(output_file, codec="libx264", fps=24)