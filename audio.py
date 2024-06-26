import os
from dotenv import load_dotenv

from openai import OpenAI
from elevenlabs import Voice, VoiceSettings, save
from elevenlabs.client import ElevenLabs

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

def generate_audio(
    input_text: str,
    output_path: str,
    type: str = "openai",
    voice_id: str = None
):
    if type == "openai":
        client = OpenAI()
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=input_text
        )
        response.write_to_file(output_path)
        return response.content
    
    elif type == "elevenlabs":

        client = ElevenLabs(
            api_key=ELEVEN_API_KEY
        )
        if voice_id is None or voice_id == "":
            voice_id = "3EjFjB3Y002QFneTx80s"

        audio = client.generate(
            text=input_text,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            ),
            stream=True
        )
        
        save(audio, output_path)
                
        # play(audio)
        
        return audio



# input_text = "A sudden death, a mystery unfolds."
# output_path = "./output/audio/_test.mp3"
# audio = generate_audio(
#     input_text,
#     output_path,
#     "elevenlabs",
#     "vwRlaUMqwnqD7g3rWVUR"
# )
