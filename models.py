from pydantic.v1 import BaseModel, Field, conlist
from typing import Union, List, Optional, Literal

class VoiceModel(BaseModel):
    # TODO: Add voice model fields
    pass

class Character(BaseModel):
    """
    Represents a character in a story.
    """
    name: str = Field(..., description="The name of the character.")

class VoiceOver(BaseModel):
    """
    can be either diegetic (i.e. dialogue spoken by a character in that shot) or non-diegetic (i.e. narration by Conan)
    """
    type: Literal["diegetic", "non-diegetic"] = Field(..., description="The type of voice over.")
    text: str = Field(..., description="The spoken text, limited to one sentence or phrase.")
    character: Character = Field(..., description="The character that is speaking: defaults to Conan if it's narration, defaults to the character in the shot if dialogue.")
    voice_model: None = Field(None, description="The voice model of the character.")
    
class Shot(BaseModel):
    id: int = Field(..., description="The unique identifier for the shot.")
    description: str = Field(..., description="A two sentence description of the shot.")
    image_generation_prompt: str = Field(..., description="""
                                        Be Specific: Detail is key. Include character attributes, setting, mood, and color schemes.
                                        Balance Creativity with Clarity: While it's important to be creative, ensure your prompt is clear and understandable to the AI.
                                        Use Descriptive Language: Vivid descriptions help the AI in visualizing and creating more accurate representations.
                                         """)
    character_in_shot: Optional[Character] = Field(None, description="The character in the shot (if any) of the description or image generation prompt.")
    # video_generation_prompt: str = Field(..., description="Camera movement.")
    voice_over: VoiceOver = Field(..., description="A list of voice overs in a trailer.")
    base_image_path: Optional[str] = Field(None, description="The path to the base image used for generating the source image for the video generation.")
    image_path: Optional[str] = Field(None, description="The path to the image file for the shot.")
    video_path: Optional[str] = Field(None, description="The path to the MP4 video file for the shot.")
    audio_path: Optional[str] = Field(None, description="The path to the MP3 audio file for the shot.")
    
    def load_from_json(self, json_path: str):
        import json
        
        with open('./output/scripts/2.json', 'r') as file:
            data = json.load(file)
        
        # TODO: Extract the first shot from the shotlist
        shot_data = data['shotlist'][0]
        
        # Populate the fields of the Shot instance
        self.id = shot_data['id']
        self.description = shot_data['description']
        self.image_generation_prompt = shot_data['image_generation_prompt']
        
        # Setup the character in the shot
        if 'character_in_shot' in shot_data:
            self.character_in_shot = Character(
                name=shot_data['character_in_shot']['name'],
            )
        
        # Setup the voice over
        self.voice_over = VoiceOver(
            type=shot_data['voice_over']['type'],
            text=shot_data['voice_over']['text'],
            character=Character(
                name=shot_data['voice_over']['character']['name'],
            ),
            voice_model=shot_data['voice_over']['voice_model'],
        )
    
    def generate_audio(self):
        """
        generates an audio file based on the voice_over
        """
        import audio
        
        input_text = self.voice_over.text
        output_path = f"./output/audio/{self.id}.mp3"
        audio = audio.generate_audio(
            input_text,
            output_path
        )
        self.audio_path = output_path
    
    def find_base_image(self):
        """
        based on the character attribute dynamically finds the corresponding base_image_path in ./assets/images
        e.g. if the character's name is "Conan", the base_image_path is "./assets/images/conan.jpeg",
        if the character's name is "Ran", the base_image_path is "./assets/images/ran.jpeg"
        ...and so on
        if the character attribute is empty, set to None
        """
        if self.character_in_shot:
            self.base_image_path = f"./assets/images/{self.character_in_shot.name.lower()}.jpeg"
        else:
            self.base_image_path = None
    
    def generate_image(self):
        """
        generates an image based on the image_generation_prompt
        """
        
        import video
        
        image = video.transform_image(self.base_image_path)
        prompt = self.image_generation_prompt
        output_path = f"./output/images/{self.id}.jpeg"
        
        if self.character_in_shot:
            video.generate_image_to_image(
                image=image,
                prompt=prompt,
                output_path=output_path
            )
        else:
            video.generate_text_to_image(prompt, output_path)
        self.image_path = output_path
    
    def generate_video(self):
        """
        generates a video based on the image_path
        """
        
        import video
        
        image = video.transform_image(self.image_path)
        output_path = f"./output/videos/{self.id}.mp4"
        
        video.generate_video_from_image(
            image=image,
            output_path=output_path
        )
        self.video_path = output_path
        
    def populate(self):
        """
        populates the shot with the necessary data
        """
        self.generate_audio()
        self.find_base_image()
        self.generate_image()
        self.generate_video()


class Script(BaseModel):
    """
    You'll want to aim for a three-act structure, however abridged, in in your trailer. This means you'll establish characters, introduce the conflict or complications, and then raise the stakes and tease the conclusion.
    The last shot of the trailer should build anticipation & intrigue for the audience.
    """
    title: str = Field(..., description="The title of the movie, starting with Detective Conan:...")
    premise: str = Field(..., description="The 2 sentence premise of the movie trailer.")
    shotlist: List[Shot] = Field(..., description="Between 15 and 20 shots, each with a description, image generation prompt, video generation prompt, and dialogue.")
    
    @classmethod
    def from_json(cls, json_path: str):
        import json
        
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        instance = cls(
            title=data['title'],
            premise=data['premise'],
            shotlist=[]
        )
        
        for shot_data in data['shotlist']:
            shot = Shot(
                id=shot_data['id'],
                description=shot_data['description'],
                image_generation_prompt=shot_data['image_generation_prompt'],
                character_in_shot=Character(
                    name=shot_data['character_in_shot']['name'],
                ) if 'character_in_shot' in shot_data else None,
                voice_over=VoiceOver(
                    type=shot_data['voice_over']['type'],
                    text=shot_data['voice_over']['text'],
                    character=Character(
                        name=shot_data['voice_over']['character']['name'],
                    ),
                    voice_model=shot_data['voice_over']['voice_model'],
                ),
                base_image_path=shot_data['base_image_path'],
                image_path=shot_data['image_path'],
                video_path=shot_data['video_path'],
                audio_path=shot_data['audio_path'],
            )
            
            instance.shotlist.append(shot)
        
        return instance
    
class Trailer(BaseModel):
    script: Script = Field(..., description="The script for the trailer.")
    # TODO
    soundtrack: str = Field(..., description="The path to the soundtrack for the trailer.")
    video_path: Optional[str] = Field(None, description="The path to the final MP4 video file for the trailer.")
    