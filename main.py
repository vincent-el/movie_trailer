from models import Script
import script
import video
import audio
import editor

news_story = """
Pennsylvania pastor survives attempted shooting during service
4 days ago
By Holly Honderich,
in Washington

Share

Contains some violence and some upsetting scenes.

1:18
Contains some violence and some upsetting scenes.

Watch: The moment pastor survives shooting attempt during sermon
A Pennsylvania pastor survived a shooting in the middle of his Sunday sermon when the attacker's gun jammed, giving congregants time to subdue him.

Footage of the attack shows pastor Glenn Germany diving behind his lectern after a man approaches, raises his arm and aims a gun at Mr Germany.

Police identified the gunman as 26-year-old Bernard Polite.

After Mr Polite's arrest, police found another man fatally shot at his North Braddock home.

The victim was identified as Derek Polite, 56. Police have not yet commented on Bernard Polite's relationship with him. Detectives from the Allegheny County Police Department's homicide unit are now handling the investigation. No charges have been filed in the shooting of the Derek Polite at this point.

The Reverend Glenn Germany, pastor at Jesus' Dwelling Place Church in North Braddock, a Pittsburgh suburb, told the BBC's US partner CBS News he believed God had saved him from the attack.

"I'm so grateful," he said. "You know, he shot. You can hear the gun click."

Mr Germany said he saw Mr Polite walk in and smile at him, but assumed he was coming to speak with another member of the church.

"But instead he came right here where I'm standing... and that's where he just pulled out the gun out," he said. "I'm looking right down the barrel of the gun."

Google Maps Jesus' Dwelling Place ChurchGoogle Maps
Jesus' Dwelling Place Church where Sunday's attack occurred
When Mr Polite's gun failed to discharge, church Deacon Clarence McCallister ran up the centre aisle and tackled him. While Mr Polite was being restrained, Mr Germany approached and took the gun.

Once police arrived, Mr Germany said Mr Polite spoke to him and apologised.

Mr Polite appeared to suffer from mental illness, Mr Germany said, and told him he heard voices. "The voices were in his head and said 'go shoot the pastor.'"

Mr Polite is facing multiple charges, including attempted homicide. He was denied bail and is being detained at a jail in Pittsburgh ahead of a preliminary hearing next week.

According to a criminal complaint obtained by WTAE, Mr Polite told police that he tried to shoot Mr Germany because "God told him to do it" and he was hoping to go to jail to clear his mind.
"""
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
