from models import Script
import script
import video
import audio
import editor

with open('./assets/news_story.md', 'r') as file:
    news_story = file.read()

script.generate_script(news_story)

story = Script.from_json('./output/scripts/script.json')

for shot in story.shotlist:
    print(shot.id)
    shot.generate_audio()
    shot.find_base_image()
    # print(shot.base_image_path)
    shot.generate_image()
    shot.generate_video()


editor.create_movie_clip(
    audio_folder = './output/audio',
    video_folder = './output/videos',
    output_file = './output/trailer.mp4',
    )
