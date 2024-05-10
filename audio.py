import os
from dotenv import load_dotenv

from openai import OpenAI
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

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
        if voice_id is None:
            voice_id = "5f5f1a7f-4b3e-4f5b-9f3e-9f9e2c1d0c4d" # shitty default, pls replace
        audio = client.generate(
            text=input_text,
            voice=Voice(
                voice_id=voice_id,
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            ),
            stream=True
        )
        
        # TODO: fix the image saving
        with open(output_path, "wb") as f:
            if type == "elevenlabs":
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
            else:
                f.write(audio)
        # play(audio)
        
        return audio



# input_text = "A sudden death, a mystery unfolds."
# output_path = "./output/audio/1.mp3"
# audio = generate_audio(input_text, output_path)



