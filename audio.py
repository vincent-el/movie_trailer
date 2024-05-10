import os
from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def generate_audio(input_text: str, output_path: str):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input_text
    )
    response.write_to_file(output_path)
    return response.content



# input_text = "A sudden death, a mystery unfolds."
# output_path = "./output/audio/1.mp3"
# audio = generate_audio(input_text, output_path)