import os
from dotenv import load_dotenv
import yaml

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from models import Script

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4-turbo")

def generate_script(news_story: str):
    template_path = "./prompt.md"

    with open(template_path, 'r') as file:
        template = file.read()

    parser = PydanticOutputParser(pydantic_object=Script)
    
    with open("./assets/characters.yml", 'r') as file:
        characters = yaml.safe_load(file)
        
    prompt = PromptTemplate(
        # template="""
        # Create a compelling narrative from the following news story:
        # "{news_story}"

        # Make absolutely sure to use the following format:
        # {format_instructions}
        # """,
        template=template,
        input_variables=["news_story", "characters"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | model | parser
    script = chain.invoke({
        "news_story": news_story,
        "characters": characters
        })
    # title = str(script['title'])
    output_path = "./output/scripts/script.json"
    
    with open(output_path, 'w') as file:
        file.write(script.json(indent=4))
    
    return f"Script generation successful. Title: {script.title}, Total Shots: {len(script.shotlist)}"
