from models import Script
import script
import video
import audio
import editor

with open('./assets/news_story.md', 'r') as file:
    news_story = file.read()

script.generate_script(news_story)
# print(script)

# 70s
story = Script.from_json('./output/scripts/script.json')


for shot in story.shotlist:
    # if shot.id == 4: 
    if shot.id in [1, 2, 3]: 
        shot.generate_audio()
        shot.find_base_image()
        shot.generate_image()
        # 40s
        shot.generate_video()
        



# import json
# story_json = json.loads(story)
# script['title']
# for item in script['shotlist']:
#     print(item['image_generation_prompt'])


editor.create_movie_clip(
    audio_folder = './output/audio',
    video_folder = './output/videos',
    output_file = './output/final_movie.mp4',
    )
